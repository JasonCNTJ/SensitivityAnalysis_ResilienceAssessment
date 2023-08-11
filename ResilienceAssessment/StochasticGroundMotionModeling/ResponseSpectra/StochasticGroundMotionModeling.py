# This file is a function to model the stochastic ground motion
# Created by Jiajun Du @ Tongji University, 27 July, 2023

import numpy as np
# import pandas as pd
import pickle
import scipy.stats as st
from scipy.stats import gamma
from scipy.optimize import minimize
import math
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def StochasticGroundMotionModeling(M, R, Vs, whichone, num=1, tn=40, F=1):
    """
    :params M: magnitude;
    :params R: distance;
    :params Vs: velocity;
    :params num: number of generated history;
    :params tn: the time of generated hishtory;
    :params F: fault type;
    :return: a acceleration file/ histroy
    
    目前，只有单个地震动被输出， 因为采用的是生成的所有随机参数组中的第一组。
    """

    # beta 系数， sigma标准差， corr相关系数
    betFile = r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\StochasticGroundMotionModeling\betsigcor.pkl'
    with open(betFile, 'rb') as file:
        beta = pickle.load(file)
        sigma = pickle.load(file)
        corr = pickle.load(file)

    #  求解p
    sigma2 = sigma[:, 0]**2 + sigma[:, 1]**2
    sigma2_sqrt = np.sqrt(sigma2)
    stv_m = np.diag(sigma2_sqrt)
    covar = stv_m @ corr @ stv_m  # 协方差矩阵
    par1 = np.array([1, F, M / 7, np.log(R / 25), np.log(Vs / 750)]).T
    pari = np.array([1, F, M / 7, R / 25, Vs / 750]).T
    v_miu1 = (beta[0, :] @ par1).T  # 平均值
    v_miu1 = np.array([v_miu1])
    v_miui = (beta[1:6,:] @ pari).T
    v_miu = np.concatenate((v_miu1, v_miui))
    # np.random.seed(1)  # 确保结果可以复现
    # num = 1000
    v = np.random.multivariate_normal(v_miu, covar, num)
    p = st.norm.cdf(v)

    # 利用 p 得到 theta
    # theta
    thetaFile = r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\StochasticGroundMotionModeling\thetacdf.pkl'
    with open(thetaFile, 'rb') as file:
        theta1_cdf = pickle.load(file)
        theta2_cdf = pickle.load(file)
        theta3_cdf = pickle.load(file)
        theta4_cdf = pickle.load(file)
        theta5_cdf = pickle.load(file)
        theta6_cdf = pickle.load(file)
    theta_cdf = {
        'theta1_cdf': theta1_cdf,
        'theta2_cdf': theta2_cdf,
        'theta3_cdf': theta3_cdf,
        'theta4_cdf': theta4_cdf,
        'theta5_cdf': theta5_cdf,
        'theta6_cdf': theta6_cdf
    }
    thetad = {}
    for i in range(6):
        cdf = []
        x = []
        cdf = theta_cdf['theta%i_cdf' % (i + 1)][:, 1]
        x = theta_cdf['theta%i_cdf' % (i + 1)][:, 0]
        thetai = []
        thetai = np.interp(p[:, i], cdf, x)
        if i == 0:
            thetai = np.exp(thetai)
        elif i == 3 or i == 4:
            thetai = 2 * np.pi * thetai
        else:
            pass
        thetad['theta%i' % (i + 1)] = thetai

    # theta1: Ia; theta2: D_5-95; theta3: t_mid; theta4: w_mid; theta5: w'; theta6: kesi_f

    theta = np.zeros((num, 6))
    for i in range(6):
        theta[:, i] = thetad['theta%i' % (i + 1)]

    # 取出第i组参数
    i = whichone
    theta_i = theta[i, :]
    
    # Known percentiles and values
    t_5_95 = theta_i[1]
    t_45 = theta_i[2]

    def objective(params):
        return (abs((gamma.ppf(0.95, params[0], scale=params[1]) -
                     gamma.ppf(0.05, params[0], scale=params[1])) - t_5_95) +
                abs(gamma.ppf(0.45, params[0], scale=params[1]) - t_45))

    params0 = np.array([1, 1])
    result = minimize(objective, params0, method='Nelder-Mead')
    params = result.x

    shape = params[0]
    scale = params[1]

    alpha2 = (shape + 1) / 2
    alpha3 = 1 / (2 * scale)
    alpha1 = np.sqrt(theta_i[0] * (2 * alpha3)**(2 * alpha2 - 1) /
                     math.gamma(2 * alpha2 - 1))

    np.seterr(divide='ignore', invalid='ignore')

    # 生成加速度时程
    tn = 40
    ti = np.arange(0.01, tn + 0.01, 0.01)
    kesi_f = theta_i[5]
    dt = 0.01
    acc = np.zeros(len(ti) + 1)

    for t in np.arange(0, tn + 0.01, 0.01):
        q_t_alpha = alpha1 * t**(alpha2 - 1) * np.exp(-1 * alpha3 * t)
        k = int(t / dt)

        # 计算su
        if k != 0:
            id = np.arange(1, k + 1)
            uid = np.random.randn(k)
            wfid = theta_i[3] + theta_i[4] * (ti[id - 1] - theta_i[2])  # 计算ti下的wf值
            hid = wfid / np.sqrt(1 - kesi_f**2) * np.exp(-kesi_f * wfid * (t - ti[id - 1])) * np.sin(wfid * np.sqrt(1 - kesi_f**2) * (t - ti[id - 1]))
            hjd2 = hid**2
            fm = np.sqrt(np.sum(hjd2))
            su = np.sum((hid / fm * uid))
            acc[k] = q_t_alpha * su
        else:
            acc[k] = 0

    # high pass filter
    xt = np.arange(0, tn + 0.01, 0.01)
    x = acc
    x[np.isnan(x)] = 0

    def myode(y, t, x, xt):
        wc = 0.1 * 2 * np.pi
        a = np.interp(t, xt, x)
        dydt = [y[1], a - 2 * wc * y[1] - wc**2 * y[0]]
        return dydt

    y0 = [0, 0]
    t = np.arange(0, tn + 0.01, 0.01)
    sol = odeint(myode, y0, t, args=(x, xt))

    wc = 0.1 * 2 * np.pi
    ACC = x - 2 * wc * sol[:, 1] - wc**2 * sol[:, 0]

    # plt.plot(t, ACC, linewidth=0.5)
    # plt.xlabel('time (s)')
    # plt.ylabel('acc (g)')
    # plt.title('acc history')
    # plt.grid(True)
    # plt.show()
    return ACC, tn


if __name__ == '__main__':
    StochasticGroundMotionModeling(6.61, 19.3, 602, 1)