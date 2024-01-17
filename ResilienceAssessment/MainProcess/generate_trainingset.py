import numpy as np
import multiprocessing as mp
import time
import func_generate_trainingset as fgt


if __name__ == '__main__':
    start_time = time.time()  # 记录开始时间
    num_processes = 16
    pool = mp.Pool(processes=num_processes)

    # 使用map来分配任务给不同进程，这里的参数是一个可迭代对象，例如range
    results = pool.map(fgt.FuncGenerateTrainingSet, range(num_processes))

    # 关闭进程池，防止新任务被提交
    pool.close()

    # 等待所有进程完成
    pool.join()
    # 将各个进程返回的元组拼接成一个大列表
    concatenated_result = []
    for result in results:
        concatenated_result.append(result)

    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    print('计算时间为', elapsed_time, 's')