# import modules
import numpy as np
import pandas as pd
import pathlib
import pickle
import multiprocessing as mp
import time
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


def ReslienceAssessment(queue, seed):
    # BASE INFORMATION
    cwdFile = pathlib.Path.cwd()
    cwdFile = cwdFile / 'ResilienceAssessment' / 'MainProcess'
    print(cwdFile)
    buildingDataFile = cwdFile /'BuildingData'
    geometryFile = buildingDataFile / 'Geometry.csv'
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
    nSample = 10
    edpOutput = np.zeros((nSample, 8))
    costOutput = np.zeros(nSample)
    np.random.seed(seed)  # 设置随机种子
    # np.random.seed(1)  # 确保结果可以复现
    Output = []
    for i in range(nSample):
        print(i)
        ACC, tn = StochasticGroundMotionModeling(7.62, 19.3, 602, 0)
        # NTHA
        dt = 0.01
        ACC = ACC.tolist()
        edpResult = NonlinearAnalysis(building, columns, beams, baseFile, ACC, dt)
        edpOutput[i, :] = edpResult
        # print(edpResult)
        data = Data()
        IDR = edpResult[:3]
        PFA = edpResult[3:7]
        frameCost, sframeCost, nframeCost, cframeCost = data.cal_repair(IDR, PFA)
        # print(frameCost)
        costOutput[i] = frameCost
    Output.append((edpOutput, costOutput))
    queue.put(Output)
    

if __name__ == '__main__':
    start_time = time.time()  # 记录开始时间
    mp.set_start_method('spawn')
    # 创建一个进程间通信的队列
    queue = mp.Queue()
    # 创建进程并执行任务
    procs = []
    np.random.seed(1)
    # ? 是否需要加上不重复？
    for i in range(8):
        seed = np.random.randint(1000)  # 生成不同的随机种子
        proc = mp.Process(target=ReslienceAssessment, args=(queue, seed))
        procs.append(proc)
    # procs = [mp.Process(target=ReslienceAssessment, args=(queue,)) for _ in range(4)]
    for p in procs:
        p.start()
    # 等待所有进程执行完毕
    for p in procs:
        p.join()
    # 从队列中获得每个进程生成的列表并合并
    result = []
    while not queue.empty():
        result.extend(queue.get())
    # print(result)
    edpReuslt, costResult = zip(*result)
    print(edpReuslt)
    print(costResult)
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    print('计算时间为', elapsed_time, 's')
