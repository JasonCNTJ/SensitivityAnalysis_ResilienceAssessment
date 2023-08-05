"""

Auxiliary file
==============================================

"""

import numpy as np


def evaluate(X, params) -> np.array:
    r"""A linear function that is used to demonstrate sensitivity indices.

    .. math::
        f(x) = a \cdot x_1 + b \cdot x_2
    """
    a, b = params

    Y = a * X[:, 0] + b * X[:, 1]

    return Y


def evaluate_test(X) -> np.array:
    r"""A linear function that is used to demonstrate sensitivity indices.

    .. math::
        f(x) = a \cdot x_1 + b \cdot x_2
    """

    Y = X[:, 0] + X[:, 1] * X[:, 2]

    return Y
