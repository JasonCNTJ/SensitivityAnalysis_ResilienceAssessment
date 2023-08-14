# import modules
import numpy as np
# import pandas as pd
# import pathlib
# import pickle
import multiprocessing as mp
import time
# module for SGMM
# from StochasticGroundMotionModeling import StochasticGroundMotionModeling
# module for NTHA
# from BuildingObject import Building_object
# from beam_component import Beam
# from column_component import Column
# from steel_material import SteelMaterial
# from nonlinear_analysis import NonlinearAnalysis
# module for seismic consequence evaluation
# from loss_calculation import Data
import resilience_assessment as ra


if __name__ == '__main__':
    start_time = time.time()  # 记录开始时间
    mp.set_start_method('spawn')
    # 创建一个进程间通信的队列
    queue = mp.Queue()
    # 创建进程并执行任务
    procs = []
    np.random.seed(1)
    # ? 是否需要加上不重复？
    for i in range(16):
        # seed = np.random.randint(1000)  # 生成不同的随机种子
        proc = mp.Process(target=ra.ResilienceAssessment, args=(queue,))
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
