import numpy as np


def linear(a: float, b: float, x: float) -> float:
    return a + b * x


def wrapped_linear(X, func=linear):
    N, D = X.shape
    results = np.empty(N)
    for i in range(N):
        a, b, x = X[i, :]
        results[i] = func(a, b, x)

    return results
