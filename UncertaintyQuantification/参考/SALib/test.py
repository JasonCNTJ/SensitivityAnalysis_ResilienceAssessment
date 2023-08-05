import numpy as np
from SALib.sample import saltelli


def linear(a: float, b: float, x: float) -> float:
    return a + b * x


def wrapped_linear(X: np.ndarray, func=linear) -> np.ndarray:
    N, D = X.shape
    results = np.empty(N)
    for i in range(N):
        a, b, x = X[i, :]
        results[i] = func(a, b, x)

    return results


problem = {
    'names': ['a', 'b', 'x'],
    'bounds': [
        [-1, 0],
        [-1, 0],
        [-1, 1],
    ],
    'num_vars': 3
}

X = saltelli.sample(problem, 64)
Y = np.empty(params.shape[0])
for i in range(params.shape[0]):
    Y[i] = wrapped_linear(params[i, :])

res = sobol.analyze(problem, Y)
res.to_df()

