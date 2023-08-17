# import modules
import numpy as np
import pandas as pd
import pathlib
import pickle
# module for SGMM
from StochasticGroundMotionModeling import StochasticGroundMotionModeling
# module for NTHA
from BuildingObject import Building_object
from beam_component import Beam
from column_component import Column
from steel_material import SteelMaterial
from nonlinear_analysis import NonlinearAnalysis
# module for seismic consequence evaluation
from loss_calculation import Data


def ResilienceAssessment(X):
    """
    :params X: a list of interested parameters.
        'names': ['M', 'R', 'V_s30', 'F', 'm_b',
                  'kesi', 'P_nsq', 'Q_con', 'M_bcj',
                  'M_gcw', 'M_wp', 'M_sc', 'M_ele',
                  'M_hvac', 'M_rf', 'S_rf', 'C_rep'],
        'bounds': [
            [6.0, 8.0], [10, 100], [600, 1500], [0, 1], [0.872, 1.128, 1, 0.1],
            [0.02, 0.05], [0, 1], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3],
            [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3],
            [0.616, 1.384, 1, 0.3], [0.005, 0.015], [0.1, 0.8], [1, 1.0/0.3]
        ],
        'dists': ['unif', 'unif', 'unif', 'unif', 'truncnorm',
                  'unif', 'unif', 'truncnorm','truncnorm',
                  'truncnorm', 'truncnorm', 'truncnorm', 'truncnorm',
                  'truncnorm', 'uniform', 'uniform', 'uniform']
    :return: Output
    """
    # BASE INFORMATION
    cwdFile = pathlib.Path.cwd()
    cwdFile = cwdFile / 'ResilienceAssessment' / 'MainProcess'
    print(cwdFile)
    buildingDataFile = cwdFile / 'BuildingData'
    # geometryFile = buildingDataFile / 'Geometry.csv'
    memberSizeFile = buildingDataFile / 'MemberSize.csv'
    loadsFile = buildingDataFile / 'Loads.csv'

    member_size = pd.read_csv(memberSizeFile)
    gravity_loads = pd.read_csv(loadsFile)
    directory = {}
    directory = {'building data': buildingDataFile}
    building = Building_object(directory, member_size, gravity_loads)

    # beams
    beamSizeFile = buildingDataFile / 'beamsectionsize.csv'
    SectionDatabaseFile = cwdFile / 'AllSectionDatabase.csv'
    SectionDatabase = pd.read_csv(SectionDatabaseFile)

    steel = SteelMaterial(yield_stress=50, ultimate_stress=65, elastic_modulus=29000,
                          Ry_value=1.1)  # Unit: ksi
    # 创建包含梁信息的嵌套字典
    beam_section_size = pd.read_csv(beamSizeFile)
    beams = {}
    length = int(building.geometry['X bay width'])
    for _, row in beam_section_size.iterrows():
        level, bay = map(int, row[:2])
        bsection_size = {'size': row[2]}
        beams.setdefault(level, {})
        beams[level].setdefault(bay, {})
        beams[level][bay] = Beam(bsection_size['size'], length, steel, SectionDatabase)

    # elastic demand
    elasticDemandFile = cwdFile / 'elastic_demand.pkl'
    with open(elasticDemandFile, 'rb') as f:
        elastic_demand = pickle.load(f)

    # column
    columnSizeFile = buildingDataFile / 'columnsectionsize.csv'
    SectionDatabaseFile = cwdFile / 'AllSectionDatabase.csv'
    SectionDatabase = pd.read_csv(SectionDatabaseFile)

    steel = SteelMaterial(yield_stress=50, ultimate_stress=65, elastic_modulus=29000,
                          Ry_value=1.1)  # Unit: ksi

    # 构建包含柱信息的嵌套字典
    column_section_size = pd.read_csv(columnSizeFile)
    columns = {}
    for _, row in column_section_size.iterrows():
        story, pier = map(int, row[:2])
        csection_size = {'size': row[2]}
        columns.setdefault(story, {})
        columns[story].setdefault(bay, {})
        axial_demand = abs(elastic_demand.dominate_load['column axial'][story, 2 * pier])
        Lx = (building.geometry['floor height'][story+1] - building.geometry['floor height'][story]).item()
        Ly = Lx
        columns[story][pier] = Column(csection_size['size'], axial_demand, Lx, Ly, steel, SectionDatabase)
    nSample, D = X.shape
    baseFile = cwdFile
    nSample = 1
    edpOutput = np.empty((nSample, 8))
    costOutput = np.empty(nSample)  # results
    # np.random.seed(seed)  # 设置随机种子
    # np.random.seed(1)  # 确保结果可以复现
    # Output = []
    for i in range(nSample):
        print(i)
        # 传递传入的参数
        M, R, V_s30, F, m_b, kesi, P_nsq, M_bcj, M_gcw, M_wp, M_sc, M_ele, M_hvac, M_rf, S_rf, C_rep = X[i, :]
        # 随机生成地震动
        ACC, tn = StochasticGroundMotionModeling(M, R, V_s30, F)
        # NTHA
        dt = 0.01
        ACC = ACC.tolist()
        edpResult = NonlinearAnalysis(building, columns, beams, baseFile, ACC, dt, m_b, kesi)
        edpOutput[i, :] = edpResult
        # print(edpResult)
        data = Data(P_nsq, M_bcj, M_gcw, M_wp, M_sc, M_ele, M_hvac)
        IDR = edpResult[:3]
        PFA = edpResult[3:7]
        RIDR = edpResult[7]
        costOut_list, costOut_mean = data.costOut(IDR, PFA, RIDR, 1000, M_rf, S_rf, C_rep)
        costOutput[i] = costOut_mean

    return costOutput
