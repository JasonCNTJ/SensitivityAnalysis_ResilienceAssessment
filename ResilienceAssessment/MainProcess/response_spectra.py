import math
import numpy as np
from numba import jit
import scipy.integrate as spi


# 用Newmark方法求解地震动下结构的反应，omg：结构自振圆频率，zeta：结构阻尼比
# ag：地震加速度值，dt：地震步长
@jit(nopython=True)
def solve_sdof_eqwave_nmk(omg, zeta, ag, dt):
    omg2 = omg * omg
    # Newmark方法参数，gama和beta，本取值代表了采用的是线加速度法,如果把beta换成0.25就是平均加速度法
    gama = 0.5
    beta = 1 / 6

    c = 2*zeta*omg  # 阻尼，除以质量m
    keq = omg2 + gama/(beta*dt)*c + 1/(beta*dt*dt)  # 等效刚度

    n = len(ag)
    u = np.zeros(n)
    v = np.zeros(n)
    a = np.zeros(n)
    u[0] = 0.0  # 初始位移设为0
    v[0] = 0.0  # 初始速度设为0
    a[0] = -ag[0]-c*v[0]-omg2*u[0]  # 利用运动方程给出时间间隔下的初始加速度

    for i in range(n-1):
        peq = (-ag[i+1] + (1/beta/dt/dt+gama/beta/dt*c)*u[i] + (1/beta/dt+(gama/beta-1)*c)*v[i]
               + ((1/2/beta-1)+dt*(gama/2/beta-1)*c)*a[i])
        u[i+1] = peq/keq
        v[i+1] = gama/beta/dt*(u[i+1]-u[i])+(1-gama/beta)*v[i]+dt*(1-gama/2/beta)*a[i]
        a[i+1] = -ag[i+1]-c*v[i+1]-omg2*u[i+1]

    umax = max(np.abs(u))
    vmax = max(np.abs(v))
    amax = omg2*umax
    return umax, vmax, amax


@jit(nopython=True)
def solve_nigam_jennings(omg, zeta, ag, dnt):
    w = omg
    h = zeta
    dt = dnt
    c = 2*h*w  # 阻尼，除以质量m
    wd = math.sqrt(1-h*h) * w
    w2 = w*w
    # w3 = w*w*w
    wddt = wd*dt
    swddt = math.sin(wddt)
    cwddt = math.cos(wddt)
    ehwt = math.exp(-h*w*dt)
    hc = h/(math.sqrt(1-h*h))
    a11 = ehwt*(hc*swddt+cwddt)
    a12 = ehwt/wd*swddt
    a21 = -w/(math.sqrt(1-h*h))*ehwt*swddt
    a22 = ehwt*(cwddt-hc*swddt)

    hc2 = (2*h*h-1)/(w*w*dt)
    hw3dt = 2*h/w/w/w/dt
    b11 = ehwt*((hc2+h/w)*swddt/wd+(hw3dt+1/w/w)*cwddt)-hw3dt
    b12 = -ehwt*(hc2*swddt/wd+hw3dt*cwddt)-1/w/w+hw3dt
    b21 = ehwt*((hc2+h/w)*(cwddt-hc*swddt)-(hw3dt+1/w/w)*(wd*swddt+h*w*cwddt))+1/w/w/dt
    b22 = -ehwt*(hc2*(cwddt-hc*swddt)-hw3dt*(wd*swddt+h*w*cwddt))-1/w/w/dt
    n = len(ag)
    u = np.zeros(n)
    v = np.zeros(n)
    a = np.zeros(n)
    u[0] = 0.0  #初始位移设为0
    v[0] = 0.0  #初始速度设为0
    a[0] = -ag[0]-c*v[0]-w2*u[0] # 利用运动方程给出时间间隔下的初始加速度
    for i in range(n-1):
        u[i+1] = a11*u[i] + a12*v[i] + b11*ag[i] + b12*ag[i+1]
        v[i+1] = a21*u[i] + a22*v[i] + b21*ag[i] + b22*ag[i+1]

    umax = max(np.abs(u))
    vmax = max(np.abs(v))
    amax = w2*umax
    return umax, vmax, amax


def integrate_acceleration(a, dt=0.01, v0=0.0, d0=0.0):
    '''
    加速度时程积分为速度、位移时程：
    采用梯形数值积分法，默认初速度、初位移为零
    '''
    v = spi.cumtrapz(a, dx=dt, initial=v0)
    d = spi.cumtrapz(v, dx=dt, initial=d0)
    return v, d
