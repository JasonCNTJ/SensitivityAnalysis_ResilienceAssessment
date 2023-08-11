# import library
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
from FragilityData import Data

# IMs: 0.175 0.425 0.675 0.925 1.175 1.425 1.675 1.925
# POC: 0       0     0    1     3     16     40    67
# IMs = np.arange(0.175,2.175,0.25)
# Poc = np.array([0, 0, 0, 1, 3, 16, 40, 67])
IM = 0.425
Poc = 16
edp_data = pd.read_excel('edp_matrix_%s.xlsx' % (str(IM)), index_col=0)
EDP = edp_data.to_numpy()
# EDP
# idr1 idr2 idr3 a0 a1 a2 a3 ridr

# collapse or not

# generate 10000 random numbers
Initial_realizations = np.random.randint(1,101,10000)
Collpase_index = Initial_realizations <= Poc
Nocollapse_index = Initial_realizations > Poc
EDP_NC = EDP[Nocollapse_index]   # 找出没有倒塌的Realizations

rows, cols = np.shape(EDP_NC)

# 计算被判定为倒塌的Realization的耗费
Replacement = ???? ####################################  ???? 待定计算
# 被判定为倒塌的Realizaitons 的数量
num_collapse = 10000 - rows
# 初始化费用矩阵
Cost_matrix = np.zeros(10000)
Cost_matrix[:num_collapse] = ReplacementCost #将重置成本填入Cost_matrix

# Instantiate data class
data = Data()

# 遍历每一次 Realization
for i in range(rows):
    # max_ridr
    max_ridr = EDP_NC[i,-1]
    objPercent = data.get_prob_resi(max_ridr)
    RIDR_realizations = np.random.randint(1,101,1)
    # NR_index = RIDR_realizations <= objPercent
    # R_index = RIDR_realizations > objPercent
    if RIDR_realizations <= objPercent:
        # 不可以修复，按照倒塌计算
        Cost_matrix[num_collapse+i] = Replacement
    elif RIDR_realizations > objPercent:
        # 可以修复
        IDR = EDP_NC[i,:3]
        PFA = EDP_NC[i,3:7]
        frameCost, sframeCost, nframeCost, cframeCost = data.cal_repair(IDR, PFA)
        Cost_matrix[num_collapse+i] = frameCost


