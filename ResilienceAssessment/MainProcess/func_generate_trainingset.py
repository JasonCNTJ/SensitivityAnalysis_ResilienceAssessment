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
# module for identifying the gm parameters
from response_spectra import solve_nigam_jennings, integrate_acceleration
# from scipy.stats import truncnorm, uniform, randint
import os
# import pyDOE2 as DOE


def FuncGenerateTrainingSet(design, results, start_index, end_index):
    """
    :params queue:
    :params seed:
    :params p:
    
    :return:
    """
    # BASE INFORMATION
    os.chdir('c:\\Users\\12734\\OneDrive\\重要文件\\2_SensitivityAnalysis\\Sensitivity-PythonCode\\sensitivity-code')
    cwdFile = pathlib.Path.cwd()
    cwdFile = cwdFile / 'ResilienceAssessment' / 'MainProcess'
    # print(cwdFile)
    buildingDataFile = cwdFile /'BuildingData'
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

    baseFile = cwdFile
    nSample = end_index - start_index
    edpOutput = np.zeros((nSample, 8))
    params = np.zeros((nSample, 15))  # 存储后续用于机器学习的参数：周期T, mb, kesi, PGA, PGV, PGD, Sd, Sv, Sa
    # np.random.seed(seed)  # 设置随机种子
    # np.random.seed(1)  # 确保结果可以复现
    Output = []
    for i in range(start_index, end_index):
        # M, R, V, F, mb, kesi = design[i, :]
        mb, kesi = design[i, :]
        # M = np.random.uniform(low=6, high=8)
        # R = np.random.uniform(low=10, high=100)
        # V = np.random.uniform(low=600, high=1500)
        # F = np.random.randint(2)
        # inputp = np.hstack((M, R, V, F))
        # ACC, tn, thetai = StochasticGroundMotionModeling(6.69, 20.3, 1223, 1)
        ACC, tn, thetai = StochasticGroundMotionModeling(M=6.69, R=20.3, Vs=1223, F=1)
        ag = ACC * 9.8
        # 求解 PGA, PGV, PGD
        PGA = ag.max()
        v, d = integrate_acceleration(ag)
        PGV = v.max()
        PGD = d.max()
        # NTHA
        dt = 0.01
        ACC = ACC.tolist()
        ACC.extend([0] * 1500)
        # # 抽样mb和kesi
        # mu = 1  # 均值
        # cv = 0.1  # 变异系数
        # lower_bound = 0.872  # 下限
        # upper_bound = 1.128  # 上限
        # sigma = mu * cv  # 计算标准差
        # # 计算截断正态分布的参数
        # a = (lower_bound - mu) / sigma
        # b = (upper_bound - mu) / sigma
        # mb = truncnorm.rvs(a, b, loc=mu, scale=sigma, size=1)
        # mb = float(mb)
        # # 生成均匀分布的随机数
        # kesi = np.random.uniform(0.02, 0.05, 1)
        # kesi = float(kesi)
        edpResult, T1 = NonlinearAnalysis(building, columns, beams, baseFile, ACC, dt, mb, kesi)
        edpOutput[i-start_index, :] = edpResult
        # 获取生成地震动的相关参数
        dnt = 0.01
        omg = 2.0 * np.pi / 1.0
        zeta = 0.05
        Sd, Sv, Sa = solve_nigam_jennings(omg, zeta, ag, dnt)
        param = np.array([T1, mb, kesi, PGA, PGV, PGD, Sd, Sv, Sa])  # 9
        param = np.hstack((param, thetai))
        # param = np.hstack((param, thetai, inputp))  # theta1: Ia; theta2: D_5-95; theta3: t_mid; theta4: w_mid; theta5: w'; theta6: kesi_f 6
        params[i-start_index] = param  # 9 + 6 + 4 = 19
    Output.append((edpOutput, params))
    results.extend(Output)
