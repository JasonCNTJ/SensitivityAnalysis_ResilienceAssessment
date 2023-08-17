# from model_definitions import wrapped_linear
from SALib import ProblemSpec
import time
import ra_func_gsa as ra
import numpy as np

if __name__ == "__main__":
    start_time = time.time()  # 记录开始时间
    sp = ProblemSpec({
        'names': ['M', 'R', 'V_s30', 'F', 'm_b',
                  'kesi', 'P_nsq', 'M_bcj',
                  'M_gcw', 'M_wp', 'M_sc', 'M_ele',
                  'M_hvac', 'M_rf', 'S_rf', 'C_rep'],
        'bounds': [
            [6.0, 8.0], [10, 100], [600, 1500], [0, 1], [0.872, 1.128, 1, 0.1],
            [0.02, 0.05], [0, 1], [0.616, 1.384, 1, 0.3],
            [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3], [0.616, 1.384, 1, 0.3],
            [0.616, 1.384, 1, 0.3], [0.005, 0.015], [0.1, 0.8], [1, 1.0/0.3]
        ],
        'dists': ['unif', 'unif', 'unif', 'unif', 'truncnorm',
                  'unif', 'unif', 'truncnorm',
                  'truncnorm', 'truncnorm', 'truncnorm', 'truncnorm',
                  'truncnorm', 'unif', 'unif', 'unif']
    })

    (
        sp.sample_sobol(2)
        .evaluate(ra.ResilienceAssessment, nprocs=16)
        .analyze_sobol()
    )
    # 采样和运行结果存储
    np.savetxt("samples.txt", sp.samples)
    np.savetxt("results.txt", sp.results)
    
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    
    print('计算时间为', elapsed_time, 's')
    print(sp)
