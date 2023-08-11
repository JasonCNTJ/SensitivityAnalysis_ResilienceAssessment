import numpy as np
import multiprocessing

def gen_value(queue):
    values = []
    for i in range(10):
        values.append(np.random.randint(100))
    queue.put(values)

if __name__ == '__main__':
    # 创建一个进程间通信的队列
    queue = multiprocessing.Queue()

    # 创建进程并执行任务
    procs = [multiprocessing.Process(target=gen_value, args=(queue,)) for _ in range(8)]
    for p in procs:
        p.start()

    # 等待所有进程执行完毕
    for p in procs:
        p.join()

    # 从队列中获取每个进程生成的列表并合并
    result = []
    while not queue.empty():
        result.extend(queue.get())

    print(result)
