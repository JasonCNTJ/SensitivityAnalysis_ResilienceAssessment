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
# from loss_calculation import Data
from loss_calculation_multioutput import Data
import os
from GPRmodel import GPRmodel


def ResilienceAssessment(X):
    """
    :params X: a list of interested parameters.
        'names': ['m_b','kesi', 'P_nsq', 'Q_con', 'M_bcj',
                  'M_gcw', 'M_wp', 'M_sc', 'M_ele',
                  'M_hvac', 'M_rf', 'S_rf', 'C_rep'],
        'bounds': [
            [0.872, 1.128, 1, 0.1], [0.02, 0.05], [0, 1], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3],
            [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3],
            [0.616, 1.384, 1, 0.3], [0.005, 0.015], [0.1, 0.8], [1, 1.0/0.3]
        ],
        'dists': ['truncnorm', 'unif', 'unif', 'truncnorm',
                  'truncnorm', 'truncnorm', 'truncnorm', 'truncnorm',
                  'truncnorm', 'unif', 'unif', 'unif']
    :return: Output
    """
    # BASE INFORMATION
    os.chdir('c:\\Users\\12734\\OneDrive\\重要文件\\2_SensitivityAnalysis\\Sensitivity-PythonCode\\sensitivity-code')
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
    # nSample = 1
    # edpOutput = np.empty((nSample, 8))
    costOutput = np.empty(nSample)  # results

    # mb, kesi, PGA, PGV, PGD, Sd, Sv, Sa, d
    param_input = np.loadtxt(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\2475year_input.txt')
    theta_set = np.loadtxt(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\地震动\2475year71\theta.txt')
    # 执行
    for i in range(nSample):
        # 传递传入的参数
        m_b, kesi, P_nsq, M_bcj, M_gcw, M_wp, M_sc, M_ele, M_hvac, M_rf, S_rf, C_rep = X[i, :]
        X_predict = np.zeros((30, 9))
        X_predict[:, 0] = m_b
        X_predict[:, 1] = kesi
        X_predict[:, 2:8] = param_input
        X_predict[:, 8] = theta_set[:, 1]
        edpResult = GPRmodel(X_predict)
        # 随机生成地震动的各个参数
        # edpResult gpr生成
        IDR = edpResult[:, :3]
        PFA = edpResult[:, 3:7]
        RIDR = edpResult[:, 7]
        P_nsq = 0.99
        data = Data(P_nsq, M_bcj, M_gcw, M_wp, M_sc, M_ele, M_hvac)
        costOut_mean = data.costOut(IDR, PFA, RIDR, M_rf, S_rf, C_rep)
        costOutput[i] = np.median(costOut_mean)
        # 监控进程
        try:
            if i % 10 == 0:
                with open('process_monitor.txt', 'w') as f:
                    f.write(str(i))
        except Exception:
            pass

    return costOutput
