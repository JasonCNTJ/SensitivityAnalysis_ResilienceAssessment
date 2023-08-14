# from model_definitions import wrapped_linear
from SALib import ProblemSpec
import time
import ra_func_gsa as ra

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
        sp.sample_sobol(2)
        .evaluate(ra.ResilienceAssessment, nprocs=16)
        .analyze_sobol()
    )
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    print('计算时间为', elapsed_time, 's')
    print(sp)