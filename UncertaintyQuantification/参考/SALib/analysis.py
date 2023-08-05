from model_definitions import wrapped_linear
from SALib import ProblemSpec


sp = ProblemSpec({
    'names': ['a', 'b', 'x'],
    'bounds': [
        [-1, 0],
        [-1, 0],
        [-1, 1],
    ],
})

if __name__ == "__main__":
    (
        sp.sample_sobol(2**6)
        .evaluate(wrapped_linear, nprocs = 2)
        .analyze_sobol(nprocs = 2)
    )
    print(sp)