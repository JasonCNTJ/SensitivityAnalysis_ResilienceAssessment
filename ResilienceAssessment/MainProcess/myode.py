import numpy as np

def myode(y, t, x, xt):
    wc = 0.1 * 2 * np.pi
    a = np.interp(t, xt, x)
    dydt = [y[1], a - 2 * wc * y[1] - wc**2 * y[0]]
    return dydt