import numpy as np


def calculate_IA(ACC):
    Ia = np.cumsum(np.pi / (2 * 9.8) * (ACC ** 2) * 0.01)
    IA = np.max(Ia)
    Ia_5 = 0.05 * IA
    Ia_95 = 0.95 * IA
    Ia_45 = 0.45 * IA
    t_5 = np.argmin(np.abs(Ia - Ia_5))
    t_95 = np.argmin(np.abs(Ia - Ia_95))
    t_45 = np.argmin(np.abs(Ia - Ia_45))
    D5_45 = (t_95 - t_5) * 0.01
    t_mid = t_45 * 0.01
    return IA, D5_45, t_mid
