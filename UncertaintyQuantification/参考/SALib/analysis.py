# from model_definitions import wrapped_linear
import numpy as np
from SALib import ProblemSpec
import time


def wrapped_linear(X):
    N, D = X.shape
    results = np.empty(N)
    for i in range(N):
        # time.sleep(1)
        a, b, x = X[i, :]
        results[i] = a + b * x
    return results


if __name__ == "__main__":
    start_time = time.time()  # 记录开始时间
    sp = ProblemSpec({
        'names': ['a', 'b', 'x'],
        'bounds': [
            [-1, 0],
            [-1, 0],
            [-1, 1],
        ],
    })
    
    (
        sp.sample_sobol(2**6)
        .evaluate(wrapped_linear, nprocs = 16)
        .analyze_pawn()
    )
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    print('计算时间为', elapsed_time, 's')
    print(sp)
    sp.heatmap()