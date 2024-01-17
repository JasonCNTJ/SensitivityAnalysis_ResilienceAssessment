from scipy.stats import lognorm
from scipy.stats import norm
import numpy as np


# Fragility Database
class Data:
    """
    """
    def __init__(self, P_nsq, M_bcj, M_gcw, M_wp, M_sc, M_ele, M_hvac):
        self.P_nsq = P_nsq
        self.M_bcj = M_bcj
        self.M_gcw = M_gcw
        self.M_wp = M_wp
        self.M_sc = M_sc
        self.M_ele = M_ele
        self.M_hvac = M_hvac
        self.componentData = {
            "1": {
                'ID': 'B2022.001',  # Curtain walls
                'STORY': [1, 2, 3],
                'UNIT': 216,
                '50thp': 0.645,
                'BETA': 0.6,
                'EDP': 'PID',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 0.0338 * self.M_gcw,
                    'DP': 0.4,
                    'LQ': 20,
                    'UQ': 100,
                    'LRC': 2060,
                    'URC': 1100,
                    'DIS': 'Lognormal',
                    'CV': 0.17
                },
                'DS2': {
                    'MD': 0.0383 * self.M_gcw,
                    'DP': 0.4,
                    'LQ': 20,
                    'UQ': 100,
                    'LRC': 2060,
                    'URC': 1100,
                    'DIS': 'Lognormal',
                    'CV': 0.17
                },
            },
            "2": {
                'ID': 'C1011.001a',  # Wall partitions
                'STORY': [1, 2, 3],
                'UNIT': 21.6,
                '50thp': 0.001,
                'BETA': 0.2,
                'EDP': 'PID',
                'CT': 'N',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.005 * self.M_wp,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 2680,
                    'URC': 1430,
                    'DIS': 'Normal',
                    'CV': 0.48
                },
                'DS2': {
                    'MD': 0.01 * self.M_wp,
                    'DP': 0.3,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 6830,
                    'URC': 3640,
                    'DIS': 'Lognormal',
                    'CV': 0.56
                },
                'DS3': {
                    'MD': 0.021 * self.M_wp,
                    'DP': 0.2,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 10500,
                    'URC': 7440,
                    'DIS': 'Lognormal',
                    'CV': 0.20
                },
            },
            "3": {
                'ID': 'C3032.001a',  # suspending ceiling
                'STORY': [1, 2, 3],
                'UNIT': 86.4,
                '50thp': 1,
                'BETA': 0.0,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 1.17 * self.M_sc,
                    'DP': 0.25,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 435,
                    'URC': 290,
                    'DIS': 'Normal',
                    'CV': 0.55
                },
                'DS2': {
                    'MD': 1.58 * self.M_sc,
                    'DP': 0.25,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 3410,
                    'URC': 2270,
                    'DIS': 'Lognormal',
                    'CV': 0.52
                },
                'DS3': {
                    'MD': 1.82 * self.M_sc,
                    'DP': 0.25,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 7010,
                    'URC': 4670,
                    'DIS': 'Lognormal',
                    'CV': 0.20
                },
            },
            "4": {
                'ID': 'C3027.002',  # raised access floor, seismically rated
                'STORY': [1, 2, 3],
                'UNIT': 162,
                '50thp': 0.75,
                'BETA': 0.2,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1.5,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 138,
                    'URC': 92,
                    'DIS': 'Normal',
                    'CV': 1.28
                },
            },
            "5": {
                'ID': 'D2021.011a',  # Cold or hot potable
                'STORY': [1, 2, 3],
                'UNIT': 0.91,
                '50thp': 0.00004,
                'BETA': 0.7,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 1.5,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 4,
                    'LRC': 319,
                    'URC': 261,
                    'DIS': 'Lognormal',
                    'CV': 0.76
                },
                'DS2': {
                    'MD': 2.6,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 4,
                    'LRC': 2920,
                    'URC': 2390,
                    'DIS': 'Lognormal',
                    'CV': 0.41
                },
            },
            "6": {
                'ID': 'D3041.012a',  # HVAC galvanized sheet metal ducting>=6
                'STORY': [1, 2, 3],
                'UNIT': 0.43,
                '50thp': 0.00002,
                'BETA': 0.2,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 1.5 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 1050,
                    'URC': 855,
                    'DIS': 'Lognormal',
                    'CV': 0.26
                },
                'DS2': {
                    'MD': 2.25 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 8750,
                    'URC': 7160,
                    'DIS': 'Lognormal',
                    'CV': 0.08
                },
            },
            "7": {
                'ID': 'D3041.011a',  # HVAC galvanized sheet metal ducting<6
                'STORY': [1, 2, 3],
                'UNIT': 1.62,
                '50thp': 0.000075,
                'BETA': 0.2,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 1.5 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 715,
                    'URC': 585,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
                'DS2': {
                    'MD': 2.25 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 6990,
                    'URC': 5720,
                    'DIS': 'Lognormal',
                    'CV': 0.1
                },
            },
            "8": {
                'ID': 'D3041.031a',  # HVAC drops / diffusers
                'STORY': [1, 2, 3],
                'UNIT': 19.44,
                '50thp': 0.009,
                'BETA': 0.5,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1.3 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 3300,
                    'URC': 2700,
                    'DIS': 'Normal',
                    'CV': 0.21
                },
            },
            "9": {
                'ID': 'D3041.041a',  # VAV box
                'STORY': [1, 2, 3],
                'UNIT': 10.8,
                '50thp': 0.002,
                'BETA': 0.2,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1.9 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 16500,
                    'URC': 13500,
                    'DIS': 'Lognormal',
                    'CV': 0.29
                },
            },
            "10": {
                'ID': 'D3034.002',  # Independent pendant lighting
                'STORY': [1, 2, 3],
                'UNIT': 648,
                '50thp': 0.015,
                'BETA': 0.3,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1.5,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 10,
                    'LRC': 990,
                    'URC': 297,
                    'DIS': 'Lognormal',
                    'CV': 0.64
                },
            },
            "11": {
                'ID': 'D4011.021a',  # fire sprinkler water piping
                'STORY': [1, 2, 3],
                'UNIT': 4.32,
                '50thp': 0.01,
                'BETA': 0.1,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 1.1,
                    'DP': 0.4,
                    'LQ': 3,
                    'UQ': 10,
                    'LRC': 385,
                    'URC': 315,
                    'DIS': 'Lognormal',
                    'CV': 0.65
                },
                'DS2': {
                    'MD': 2.4,
                    'DP': 0.5,
                    'LQ': 3,
                    'UQ': 10,
                    'LRC': 2920,
                    'URC': 2390,
                    'DIS': 'Lognormal',
                    'CV': 0.41
                },
            },
            "12": {
                'ID': 'D4011.031a',  # fire sprinkler drop standard threaded steel
                'STORY': [1, 2, 3],
                'UNIT': 1.94,
                '50thp': 0.009,
                'BETA': 0.2,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 0.75,
                    'DP': 0.4,
                    'LQ': 2,
                    'UQ': 5,
                    'LRC': 550,
                    'URC': 450,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
                'DS2': {
                    'MD': 0.95,
                    'DP': 0.4,
                    'LQ': 2,
                    'UQ': 5,
                    'LRC': 550,
                    'URC': 450,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
            },
            "13": {
                'ID': 'C2011.001b',  # 楼梯
                'STORY': [1, 2, 3],
                'UNIT': 2.16,
                '50thp': 0.0001,
                'BETA': 0.2,
                'EDP': 'PID',
                'CT': 'N',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.005,
                    'DP': 0.6,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 4340,
                    'URC': 1300,
                    'DIS': 'Normal',
                    'CV': 0.46
                },
                'DS2': {
                    'MD': 0.017,
                    'DP': 0.6,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 11100,
                    'URC': 3330,
                    'DIS': 'Normal',
                    'CV': 0.49
                },
                'DS3': {
                    'MD': 0.028,
                    'DP': 0.45,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 37600,
                    'URC': 11300,
                    'DIS': 'Lognormal',
                    'CV': 0.10
                },
            },
            "14": {
                'ID': 'D5012.021a',  # Low voltage switchgear
                'STORY': [1, 2, 3],
                'UNIT': 0.03,
                '50thp': 0.0003,
                'BETA': 0.4,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1.28,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 10200,
                    'URC': 8350,
                    'DIS': 'Lognormal',
                    'CV': 0.16
                },
            },
            "15": {
                'ID': 'D1014.011-1',  # TRACTION ELEVATOR-ds1
                'STORY': [1],
                'UNIT': 1.81,
                '50thp': 0.000028,
                'BETA': 0.7,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'P': 0.26,
                    'MD': 0.39 * self.M_ele,
                    'DP': 0.45,
                    'LQ': 5,
                    'UQ': 10,
                    'LRC': 8800,
                    'URC': 2640,
                    'DIS': 'Lognormal',
                    'CV': 0.87
                },
            },
            "16": {
                'ID': 'D1014.011-2',  # TRACTION ELEVATOR-ds2
                'STORY': [1],
                'UNIT': 1.81,
                '50thp': 0.000028,
                'BETA': 0.7,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'P': 0.79,
                    'MD': 0.39 * self.M_ele,
                    'DP': 0.45,
                    'LQ': 5,
                    'UQ': 10,
                    'LRC': 37400,
                    'URC': 11200,
                    'DIS': 'Normal',
                    'CV': 0.28
                },
            },
            "17": {
                'ID': 'D1014.011-3',  # TRACTION ELEVATOR-ds3
                'STORY': [1],
                'UNIT': 1.81,
                '50thp': 0.000028,
                'BETA': 0.7,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'P': 0.68,
                    'MD': 0.39 * self.M_ele,
                    'DP': 0.45,
                    'LQ': 5,
                    'UQ': 10,
                    'LRC': 32000,
                    'URC': 9600,
                    'DIS': 'Normal',
                    'CV': 0.41
                },
            },
            "18": {
                'ID': 'D1014.011-4',  # TRACTION ELEVATOR-ds4
                'STORY': [1],
                'UNIT': 1.81,
                '50thp': 0.000028,
                'BETA': 0.7,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'P': 0.17,
                    'MD': 0.39 * self.M_ele,
                    'DP': 0.45,
                    'LQ': 5,
                    'UQ': 10,
                    'LRC': 5000,
                    'URC': 1500,
                    'DIS': 'Normal',
                    'CV': 0.49
                },
            },
            "19": {
                'ID': 'D3031.011a',  # chiller
                'STORY': [1],
                'UNIT': 2.46,
                '50thp': 0.00285,
                'BETA': 0.1,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 0.2 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 50800,
                    'URC': 41600,
                    'DIS': 'Lognormal',
                    'CV': 0.18
                },
            },
            "20": {
                'ID': 'D3031.021a',  # cooling tower
                'STORY': [3],
                'UNIT': 2.46,
                '50thp': 0.00285,
                'BETA': 0.1,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 0.5 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 26100,
                    'URC': 21300,
                    'DIS': 'Lognormal',
                    'CV': 0.17
                },
            },
            "21": {
                'ID': 'D3052.011a',  # air handling unit 3?
                'STORY': [1, 2, 3],
                'UNIT': 3.78,
                '50thp': 0.7,
                'BETA': 0.2,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 0.25 * self.M_hvac,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 11330,
                    'URC': 9282,
                    'DIS': 'Lognormal',
                    'CV': 0.16
                },
            },
            "22": {
                'ID': 'D5012.013a',  # motor control center
                'STORY': [1],
                'UNIT': 2.59,
                '50thp': 4E-05,
                'BETA': 0.5,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 0.73,
                    'DP': 0.45,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 4570,
                    'URC': 3740,
                    'DIS': 'Normal',
                    'CV': 0.18
                },
            },
            "23": {
                'ID': 'B1031.011c',  # steel column base plates
                'STORY': [1],
                'UNIT': 20,
                '50thp': 1,
                'BETA': 0,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.04,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 1400,
                    'URC': 860,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
                'DS2': {
                    'MD': 0.07,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 37500,
                    'URC': 26500,
                    'DIS': 'Lognormal',
                    'CV': 0.31
                },
                'DS3': {
                    'MD': 0.1,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 47500,
                    'URC': 33700,
                    'DIS': 'Lognormal',
                    'CV': 0.27
                },
            },
            "24": {
                'ID': 'B1035.002',  # PN RBS >=30 ONE SIDE
                'STORY': [1, 2],
                'UNIT': 8,
                '50thp': 1,
                'BETA': 0,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.03 * self.M_bcj,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 23000,
                    'URC': 15600,
                    'DIS': 'Normal',
                    'CV': 0.33
                },
                'DS2': {
                    'MD': 0.04 * self.M_bcj,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 40500,
                    'URC': 27500,
                    'DIS': 'Normal',
                    'CV': 0.28
                },
                'DS3': {
                    'MD': 0.05 * self.M_bcj,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 40500,
                    'URC': 27500,
                    'DIS': 'Lognormal',
                    'CV': 0.28
                },
            },
            "25": {
                'ID': 'B1035.012',  # PN RBS >=30 BOTH SIDE
                'STORY': [1, 2],
                'UNIT': 12,
                '50thp': 1,
                'BETA': 0,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.03,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 40000,
                    'URC': 27200,
                    'DIS': 'Normal',
                    'CV': 0.31
                },
                'DS2': {
                    'MD': 0.04,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 73100,
                    'URC': 49700,
                    'DIS': 'Normal',
                    'CV': 0.25
                },
                'DS3': {
                    'MD': 0.05,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 73100,
                    'URC': 49700,
                    'DIS': 'Normal',
                    'CV': 0.25
                },
            },
            "26": {
                'ID': 'B1035.001',  # PN RBS <=27 ONE SIDE
                'STORY': [3],
                'UNIT': 8,
                '50thp': 1,
                'BETA': 0,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.03,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 21800,
                    'URC': 14800,
                    'DIS': 'Normal',
                    'CV': 0.35
                },
                'DS2': {
                    'MD': 0.04,
                    'DP': 0.3,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 36600,
                    'URC': 24900,
                    'DIS': 'Normal',
                    'CV': 0.31
                },
                'DS3': {
                    'MD': 0.05,
                    'DP': 0.3,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 36600,
                    'URC': 24900,
                    'DIS': 'Normal',
                    'CV': 0.31
                },
            },
            "27": {
                'ID': 'B1035.011',  # PN RBS <=27 BOTH SIDE
                'STORY': [3],
                'UNIT': 12,
                '50thp': 1,
                'BETA': 0,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.03,
                    'DP': 0.3,
                    'LQ': 3,
                    'UQ': 7,
                    'LRC': 37500,
                    'URC': 25500,
                    'DIS': 'Normal',
                    'CV': 0.33
                },
                'DS2': {
                    'MD': 0.04,
                    'DP': 0.3,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 65400,
                    'URC': 44500,
                    'DIS': 'Normal',
                    'CV': 0.28
                },
                'DS3': {
                    'MD': 0.05,
                    'DP': 0.3,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 65400,
                    'URC': 44500,
                    'DIS': 'Normal',
                    'CV': 0.28
                },
            },
        }

    # get all component data
    def get_all(self):

        return self.componentData

    # get by component type
    def get_type(self, compType):
        componentList = []
        for i in self.componentData:
            if self.componentData[i]['CT'] == compType:
                componentList.append(self.componentData[i])
        return componentList

    # get by ID
    def get_id(self, ID):
        componentList = []
        for i in self.componentData:
            if self.componentData[i]['ID'] == ID:
                componentList.append(self.componentData[i])

        return componentList

    # calculate interpolated cost for number of components
    def cal_interp(self, index, ds):
        comp = self.componentData['%s' % index]
        unit = comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
        lq = comp['DS%s' % ds]['LQ']
        uq = comp['DS%s' % ds]['UQ']
        lrc = comp['DS%s' % ds]['LRC']
        urc = comp['DS%s' % ds]['URC']

        if unit <= lq:
            singleCost = lrc
        elif unit >= uq:
            singleCost = urc
        else:
            singleCost = lrc - (unit - lq) * (lrc - urc) / (uq - lq)

        return singleCost

    # Get the probability of DSi according to EDP and component data
    def cal_prob(self, edp, index):
        comp = self.componentData['%s' % index]
        dsNum = comp['DS_NUM']
        if dsNum == 1:
            mean = comp['DS1']['MD']
            beta = comp['DS1']['DP']
            edpPercent = self.lognormal_func(mean, beta, edp)
            #               P(<=DS1)      P(>DS1)
            perList = [1 - edpPercent, edpPercent]
            pds = [round(perList[1] * 100)]

        elif dsNum == 2:
            edpPercent1 = self.lognormal_func(comp['DS1']['MD'],
                                              comp['DS1']['DP'], edp)
            edpPercent2 = self.lognormal_func(comp['DS2']['MD'],
                                              comp['DS2']['DP'], edp)
            #           P(<=DS1)       P(DS1<=DS<=DS2)          P(>=DS2)
            perList = [1 - edpPercent1, edpPercent1 - edpPercent2, edpPercent2]
            pds1 = round(perList[1] * 100)
            pds2 = pds1 + round(perList[2] * 100)
            pds = [pds1, pds2]

        elif dsNum == 3:
            edpPercent1 = self.lognormal_func(comp['DS1']['MD'],
                                              comp['DS1']['DP'], edp)
            edpPercent2 = self.lognormal_func(comp['DS2']['MD'],
                                              comp['DS2']['DP'], edp)
            edpPercent3 = self.lognormal_func(comp['DS3']['MD'],
                                              comp['DS3']['DP'], edp)
            perList = [
                1 - edpPercent1, edpPercent1 - edpPercent2,
                edpPercent2 - edpPercent3, edpPercent3
            ]
            pds1 = round(perList[1] * 100)
            pds2 = pds1 + round(perList[2] * 100)
            pds3 = pds2 + round(perList[3] * 100)
            pds = [pds1, pds2, pds3]
        else:
            perList = []
            pds = []
            print('There is something wrong in fc_get_prob!')

        return pds

    def lognormal_func(self, u, b, obj):
        dist = lognorm(s=b, scale=u)
        x = np.linspace(0, 2 * obj, 300)
        y = dist.cdf(x)
        objPercent = np.interp(obj, x, y)

        return objPercent

    # get repair consequence according to distribution
    def get_random_comp_cost(self, index, ds, cost, nRepair):
        """
        """
        comp = self.componentData['%s' % index]
        if comp['DS%s' % ds]['DIS'] == 'Normal':
            randomCost = np.random.normal(cost, comp['DS%s' % ds]['CV'] * cost, nRepair)
        else:
            randomCost = np.random.lognormal(np.log(cost), comp['DS%s' % ds]['CV'], nRepair)

        return randomCost

    # max_ridr for prob : no repair
    def get_prob_resi(self, max_ridr, M_rf, S_rf):
        mean = M_rf
        stddev = S_rf
        dist = lognorm(s=stddev, scale=mean)
        x = np.linspace(0, max_ridr * 2, 200)
        y = dist.cdf(x)
        objPercent = np.interp(max_ridr, x, y)
        objPercent = round(objPercent * 100)

        return objPercent

    # 根据EDP计算某层单个构件对应的修复费用
    def cal_comp_repair(self, story, edp, index, nRepair, worstCase):
        comp = self.componentData['%s' % index]
        # 如果该楼层有这一构件，则对修复费用进行计算，否则返回0
        if story in comp['STORY']:
            pds = self.cal_prob(edp, index)  # 'index' 构件编号
            ds = len(pds)  # damage state 的数量
            compCost = np.zeros(nRepair)
            if worstCase:
                if ds == 1:
                    singleCost = self.cal_interp(index, 1)
                    randomCost = self.get_random_comp_cost(index, 1, singleCost, nRepair)
                    compCost = randomCost * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                if ds == 2:
                    singleCost = self.cal_interp(index, 2)
                    randomCost = self.get_random_comp_cost(index, 2, singleCost, nRepair)
                    compCost = randomCost * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                if ds == 3:
                    singleCost = self.cal_interp(index, 3)
                    randomCost = self.get_random_comp_cost(index, 3, singleCost, nRepair)
                    compCost = randomCost * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
            else:
                if index >= 15 and index <= 18:
                    nNoZero = int(pds[0] / 100 * nRepair)
                    if nNoZero != 0:
                        singleCost = self.cal_interp(index, 1)
                        randomCost = self.get_random_comp_cost(index, 1, singleCost, nNoZero)
                        compCost[:nNoZero] = randomCost * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                    np.random.shuffle(compCost)  # 混排
                    compCost = compCost * comp['DS1']['P']
                else:
                    if ds == 1:
                        nNoZero = int(pds[0] / 100 * nRepair)
                        if nNoZero != 0:
                            singleCost = self.cal_interp(index, 1)
                            randomCost = self.get_random_comp_cost(index, 1, singleCost, nNoZero)
                            compCost[:nNoZero] = randomCost * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                        np.random.shuffle(compCost)  # 混排

                    if ds == 2:
                        nNoZero1 = int(pds[0] / 100 * nRepair)
                        if nNoZero1 != 0:
                            singleCost1 = self.cal_interp(index, 1)
                            randomCost1 = self.get_random_comp_cost(index, 1, singleCost1, nNoZero1)
                            compCost[:nNoZero1] = randomCost1 * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                        nNoZero2 = int((pds[1] - pds[0]) / 100 * nRepair)
                        if nNoZero2 != 0:
                            singleCost2 = self.cal_interp(index, 2)
                            randomCost2 = self.get_random_comp_cost(index, 2, singleCost2, nNoZero2)
                            compCost[nNoZero1:nNoZero1 + nNoZero2] = randomCost2 * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                        np.random.shuffle(compCost)  # 混排
                        # print(compCost)

                    if ds == 3:
                        nNoZero1 = int(pds[0] / 100 * nRepair)
                        if nNoZero1 != 0:
                            singleCost1 = self.cal_interp(index, 1)
                            randomCost1 = self.get_random_comp_cost(index, 1, singleCost1, nNoZero1)
                            compCost[:nNoZero1] = randomCost1 * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                        nNoZero2 = int((pds[1] - pds[0]) / 100 * nRepair)
                        if nNoZero2 != 0:
                            singleCost2 = self.cal_interp(index, 2)
                            randomCost2 = self.get_random_comp_cost(index, 2, singleCost2, nNoZero2)
                            compCost[nNoZero1:nNoZero1 + nNoZero2] = randomCost2 * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                        nNoZero3 = int((pds[2] - pds[1]) / 100 * nRepair)
                        if nNoZero3 != 0:
                            nNoZeroA = nNoZero1 + nNoZero2 + nNoZero3
                            if nNoZeroA >= nRepair:
                                nNoZero3 = nRepair - nNoZero1 - nNoZero2
                            singleCost3 = self.cal_interp(index, 3)
                            randomCost3 = self.get_random_comp_cost(index, 3, singleCost3, nNoZero3)
                            compCost[nNoZero1 + nNoZero2:nNoZero1 + nNoZero2 + nNoZero3] = randomCost3 * comp['UNIT'] / comp['50thp'] * np.exp(np.log(comp['50thp']) + comp['BETA'] * norm.ppf(self.P_nsq))
                        np.random.shuffle(compCost)   # 混排
        else:
            compCost = np.zeros(nRepair)

        return compCost

    # 输出此Realization下的IDR 和 PFA
    def cal_repair(self, IDR, PFA, nRepair, worstCase=0):
        """
        :param nRepair: 可修复的实现次数；
        """
        sCompCostList = np.zeros((3, nRepair))
        nCompCostList = np.zeros((3, nRepair))
        cCompCostList = np.zeros((3, nRepair))
        storyCostList = np.zeros((3, nRepair))
        #                   1 2 3
        for floor in range(1, 4):  # 层 迭代
            # single floor repair cost
            sCompCost = np.zeros(nRepair)  # 结构构件
            nCompCost = np.zeros(nRepair)  # 非结构构件
            cCompCost = np.zeros(nRepair)  # 内容物
            storyCost = np.zeros(nRepair)  # 整层

            for n in range(1, len(self.componentData) + 1):  # 构件迭代

                # PID 构件
                if self.componentData['%s' % n]['EDP'] == 'PID':
                    edp_pidr = IDR[floor - 1]
                    compCost = self.cal_comp_repair(floor, edp_pidr, n, nRepair, worstCase)
                    if self.componentData['%s' % n]['CT'] == 'S':
                        sCompCost += compCost
                    elif self.componentData['%s' % n]['CT'] == 'N':
                        nCompCost += compCost
                    elif self.componentData['%s' % n]['CT'] == 'C':
                        cCompCost += compCost
                    storyCost += compCost

                # PFA
                elif self.componentData['%s' % n]['EDP'] == 'PFA':
                    edp_pfal = PFA[floor - 1]
                    edp_pfau = PFA[floor]
                    compCostl = self.cal_comp_repair(floor - 1, edp_pfal, n, nRepair, worstCase)  # 依据底部加速度的构件
                    compCostu = self.cal_comp_repair(floor, edp_pfau, n, nRepair, worstCase)
                    compCost = compCostl + compCostu  # 汇总一层天花板和地板的加速度
                    if self.componentData['%s' % n]['CT'] == 'S':
                        sCompCost += compCost
                    elif self.componentData['%s' % n]['CT'] == 'N':
                        nCompCost += compCost
                    elif self.componentData['%s' % n]['CT'] == 'C':
                        cCompCost += compCost
                    storyCost += compCost

            sCompCostList[floor - 1] = sCompCost
            nCompCostList[floor - 1] = nCompCost
            cCompCostList[floor - 1] = cCompCost
            storyCostList[floor - 1] = storyCost

        frameCost = np.sum(storyCostList, axis=0)
        sframeCost = np.sum(sCompCostList, axis=0)
        nframeCost = np.sum(nCompCostList, axis=0)
        cframeCost = np.sum(cCompCostList, axis=0)

        return frameCost, sframeCost, nframeCost, cframeCost

    def costOut(self, IDR, PFA, RIDR, nSample, M_rf, S_rf, C_rep):
        """
        :param IDR: 层间位移角
        :param PFA: 峰值层加速度
        :param RIDR: 残余层间位移角
        :param costReplace: 重置成本
        :param nSample: 采样数目
        """
        Output_list = np.zeros(nSample)
        # calculate the maximum repair cost potential of the components
        IDR_m = np.array([10, 10, 10])
        PFA_m = np.array([100, 100, 100, 100])
        maxRepairCost, _, _, _ = self.cal_repair(IDR_m, PFA_m, 1000, worstCase=1)
        maxRepairCost = np.max(maxRepairCost)
        costReplace = C_rep * maxRepairCost
        # 判断是否倒塌
        maxIDR = IDR.max()
        if maxIDR >= 0.1:
            Output_mean = costReplace

        else:
            # 因为残余层间位移角而无法修复的概率
            probNoRepair = self.get_prob_resi(RIDR, M_rf, S_rf) / 100
            nNoRepair = int(nSample * probNoRepair)
            Output_list[:nNoRepair] = costReplace
            # 可修复的数目
            nRepair = nSample - nNoRepair
            frameCost, _, _, _ = self.cal_repair(IDR, PFA, nRepair, worstCase=0)
            Output_list[nNoRepair:] = frameCost
            np.random.shuffle(Output_list)  # 混排
            Output_mean = np.mean(Output_list)
        return Output_list, Output_mean
