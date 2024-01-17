from scipy.stats import lognorm
import numpy as np


# Fragility Database
class Data:
    def __init__(self):
        self.componentData = {
            "1": {
                'ID': 'B2022.001',
                'STORY': [1, 2, 3],
                'UNIT': 108,
                'EDP': 'PID',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 0.0338,
                    'DP': 0.4,
                    'LQ': 20,
                    'UQ': 100,
                    'LRC': 2060,
                    'URC': 1100,
                    'DIS': 'Lognormal',
                    'CV': 0.17
                },
                'DS2': {
                    'MD': 0.0383,
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
                'ID': 'B3011.011',
                'STORY': [1, 2, 3],
                'UNIT': 69,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 1.1,
                    'DP': 0.4,
                    'LQ': 13,
                    'UQ': 130,
                    'LRC': 840,
                    'URC': 490,
                    'DIS': 'Lognormal',
                    'CV': 0.58
                },
                'DS2': {
                    'MD': 1.4,
                    'DP': 0.4,
                    'LQ': 13,
                    'UQ': 130,
                    'LRC': 2220,
                    'URC': 1180,
                    'DIS': 'Lognormal',
                    'CV': 0.31
                },
            },
            "3": {
                'ID': 'C1011.001a',
                'STORY': [1, 2, 3],
                'UNIT': 26,
                'EDP': 'PID',
                'CT': 'N',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.005,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 2680,
                    'URC': 1430,
                    'DIS': 'Normal',
                    'CV': 0.48
                },
                'DS2': {
                    'MD': 0.01,
                    'DP': 0.3,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 6830,
                    'URC': 3640,
                    'DIS': 'Lognormal',
                    'CV': 0.56
                },
                'DS3': {
                    'MD': 0.021,
                    'DP': 0.2,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 10500,
                    'URC': 7440,
                    'DIS': 'Lognormal',
                    'CV': 0.20
                },
            },
            "4": {
                'ID': 'C3011.001a',
                'STORY': [1, 2, 3],
                'UNIT': 8,
                'EDP': 'PID',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 0.0021,
                    'DP': 0.6,
                    'LQ': 1,
                    'UQ': 3,
                    'LRC': 3240,
                    'URC': 2160,
                    'DIS': 'Lognormal',
                    'CV': 0.15
                },
            },
            "5": {
                'ID': 'C3032.001a',
                'STORY': [1, 2, 3],
                'UNIT': 86,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 1.17,
                    'DP': 0.25,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 435,
                    'URC': 290,
                    'DIS': 'Normal',
                    'CV': 0.55
                },
                'DS2': {
                    'MD': 1.58,
                    'DP': 0.25,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 3410,
                    'URC': 2270,
                    'DIS': 'Lognormal',
                    'CV': 0.52
                },
                'DS3': {
                    'MD': 1.82,
                    'DP': 0.25,
                    'LQ': 1,
                    'UQ': 10,
                    'LRC': 7010,
                    'URC': 4670,
                    'DIS': 'Lognormal',
                    'CV': 0.20
                },
            },
            "6": {
                'ID': 'D2021.011a',
                'STORY': [1, 2, 3],
                'UNIT': 2,
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
            "7": {
                'ID': 'D3041.011a',
                'STORY': [1, 2, 3],
                'UNIT': 1,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 2,
                'DS1': {
                    'MD': 1.5,
                    'DP': 0.4,
                    'LQ': 1,
                    'UQ': 5,
                    'LRC': 715,
                    'URC': 585,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
                'DS2': {
                    'MD': 2.25,
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
                'ID': 'D3041.031a',
                'STORY': [1, 2, 3],
                'UNIT': 17,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1.3,
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
                'ID': 'D3041.041a',
                'STORY': [1, 2, 3],
                'UNIT': 9,
                'EDP': 'PFA',
                'CT': 'N',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1.9,
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
                'ID': 'D4011.021a',
                'STORY': [1, 2, 3],
                'UNIT': 5,
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
            "11": {
                'ID': 'D4011.031a',
                'STORY': [1, 2, 3],
                'UNIT': 3,
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
            "12": {
                'ID': 'C2011.001b',  # 楼梯
                'STORY': [1, 2, 3],
                'UNIT': 3,
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
            "13": {
                'ID': 'E2022.021',
                'STORY': [1, 2, 3],
                'UNIT': 20,
                'EDP': 'PFA',
                'CT': 'C',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 2.5,
                    'DP': 0.5,
                    'LQ': 10,
                    'UQ': 50,
                    'LRC': 150,
                    'URC': 120,
                    'DIS': 'Lognormal',
                    'CV': 0.3
                },
            },
            "14": {
                'ID': 'E2022.022',
                'STORY': [1, 2, 3],
                'UNIT': 40,
                'EDP': 'PFA',
                'CT': 'C',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1,
                    'DP': 0.5,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 1500,
                    'URC': 1200,
                    'DIS': 'Lognormal',
                    'CV': 0.35
                },
            },
            "15": {
                'ID': 'E2022.102b',
                'STORY': [1, 2, 3],
                'UNIT': 40,
                'EDP': 'PFA',
                'CT': 'C',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 0.8,
                    'DP': 0.4,
                    'LQ': 10,
                    'UQ': 50,
                    'LRC': 300,
                    'URC': 250,
                    'DIS': 'Lognormal',
                    'CV': 0.3
                },
            },
            "16": {
                'ID': 'E2022.020',
                'STORY': [1, 2, 3],
                'UNIT': 50,
                'EDP': 'PFA',
                'CT': 'C',
                'DS_NUM': 1,
                'DS1': {
                    'MD': 1,
                    'DP': 0.4,
                    'LQ': 20,
                    'UQ': 100,
                    'LRC': 200,
                    'URC': 160,
                    'DIS': 'Lognormal',
                    'CV': 0.3
                },
            },
            "17": {
                'ID': 'B1031.001',
                'STORY': [1, 2, 3],
                'UNIT': 8,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.04,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 16536,
                    'URC': 10176,
                    'DIS': 'Normal',
                    'CV': 0.37
                },
                'DS2': {
                    'MD': 0.08,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 15564,
                    'URC': 11025,
                    'DIS': 'Normal',
                    'CV': 0.38
                },
                'DS3': {
                    'MD': 0.11,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 15264,
                    'URC': 10812,
                    'DIS': 'Normal',
                    'CV': 0.38
                },
            },
            "18": {
                'ID': 'B1031.011a',
                'STORY': [1],
                'UNIT': 4,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.04,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 1270,
                    'URC': 780,
                    'DIS': 'Lognormal',
                    'CV': 0.41
                },
                'DS2': {
                    'MD': 0.07,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 31500,
                    'URC': 22300,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
                'DS3': {
                    'MD': 0.1,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 36700,
                    'URC': 26000,
                    'DIS': 'Lognormal',
                    'CV': 0.34
                },
            },
            "19": {
                'ID': 'B1031.011b',
                'STORY': [1],
                'UNIT': 8,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.04,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 1320,
                    'URC': 810,
                    'DIS': 'Lognormal',
                    'CV': 0.39
                },
                'DS2': {
                    'MD': 0.07,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 33900,
                    'URC': 24000,
                    'DIS': 'Lognormal',
                    'CV': 0.34
                },
                'DS3': {
                    'MD': 0.1,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 20,
                    'LRC': 41500,
                    'URC': 29400,
                    'DIS': 'Lognormal',
                    'CV': 0.31
                },
            },
            "20": {
                'ID': 'B1031.011c',
                'STORY': [1],
                'UNIT': 8,
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
            "21": {
                'ID': 'B1035.042',
                'STORY': [1, 2],
                'UNIT': 8,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.017,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 15700,
                    'URC': 10400,
                    'DIS': 'Normal',
                    'CV': 0.36
                },
                'DS2': {
                    'MD': 0.025,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 18400,
                    'URC': 12225,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
                'DS3': {
                    'MD': 0.03,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 17500,
                    'URC': 11600,
                    'DIS': 'Lognormal',
                    'CV': 0.34
                },
            },
            "22": {
                'ID': 'B1035.052',
                'STORY': [1, 2],
                'UNIT': 8,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.017,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 21550,
                    'URC': 14400,
                    'DIS': 'Normal',
                    'CV': 0.36
                },
                'DS2': {
                    'MD': 0.025,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 28750,
                    'URC': 19150,
                    'DIS': 'Normal',
                    'CV': 0.35
                },
                'DS3': {
                    'MD': 0.03,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 28700,
                    'URC': 19100,
                    'DIS': 'Normal',
                    'CV': 0.33
                },
            },
            "23": {
                'ID': 'B1035.041',
                'STORY': [3],
                'UNIT': 8,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.017,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 14950,
                    'URC': 9937.5,
                    'DIS': 'Normal',
                    'CV': 0.35
                },
                'DS2': {
                    'MD': 0.025,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 18400,
                    'URC': 12225,
                    'DIS': 'Lognormal',
                    'CV': 0.37
                },
                'DS3': {
                    'MD': 0.03,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 17500,
                    'URC': 11600,
                    'DIS': 'Lognormal',
                    'CV': 0.34
                },
            },
            "24": {
                'ID': 'B1035.051',
                'STORY': [3],
                'UNIT': 8,
                'EDP': 'PID',
                'CT': 'S',
                'DS_NUM': 3,
                'DS1': {
                    'MD': 0.017,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 21550,
                    'URC': 14400,
                    'DIS': 'Normal',
                    'CV': 0.36
                },
                'DS2': {
                    'MD': 0.025,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 24250,
                    'URC': 16150,
                    'DIS': 'Normal',
                    'CV': 0.31
                },
                'DS3': {
                    'MD': 0.03,
                    'DP': 0.4,
                    'LQ': 5,
                    'UQ': 30,
                    'LRC': 22700,
                    'URC': 15100,
                    'DIS': 'Normal',
                    'CV': 0.33
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
        unit = comp['UNIT']
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

    # # calculate the repair consequence for single component
    # def cal_comp_repair(self, index):
    #     comp = self.componentData['%s' % index]
    #     dsNum = comp['DS_NUM']
    #     singleCost = self.cal_interp(index, dsNum)  # ???
    #     allCost = self.get_random_comp_cost(
    #         index,
    #         dsNum,
    #         singleCost,  # ???
    #     ) * len(comp['STORY']) * comp['UNIT']

    #     return allCost

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

    # ???
    # CDF
    # u  = median, b = std, obj = edp in cdf
    def lognormal_func(self, u, b, obj):
        dist = lognorm(s=b, scale=u)
        x = np.linspace(0, 2 * obj, 300)
        y = dist.cdf(x)
        objPercent = np.interp(obj, x, y)

        return objPercent

    #

    # get repair consequence according to distribution
    def get_random_comp_cost(self, index, ds, cost):
        # print(cost)
        comp = self.componentData['%s' % index]
        if comp['DS%s' % ds]['DIS'] == 'Normal':
            randomCost = np.random.normal(cost, comp['DS%s' % ds]['CV'] * cost,
                                          1)
        else:
            randomCost = np.random.lognormal(np.log(cost),
                                             comp['DS%s' % ds]['CV'], 1)

        return randomCost

    # max_ridr for prob : no repair
    def get_prob_resi(self, max_ridr):
        mean = 0.01
        stddev = 0.3
        dist = lognorm(s=stddev, scale=mean)
        x = np.linspace(0, max_ridr * 2, 200)
        y = dist.cdf(x)
        objPercent = np.interp(max_ridr, x, y)
        objPercent = round(objPercent * 100)

        return objPercent

    # 根据EDP计算某层单个构件对应的修复费用
    def cal_comp_repair(self, story, edp, index):

        comp = self.componentData['%s' % index]
        # 如果该楼层有这一构件，则对修复费用进行计算，否则返回0
        if story in comp['STORY']:
            pds = self.cal_prob(edp, index)  #'index' 构件编号
            ds = len(pds)  # damage state 的数量
            point = np.random.randint(1, 101, 1)

            if ds == 1:
                if point[0] < pds[0]:  #                  ds1
                    singleCost = self.cal_interp(index, 1)
                    randomCost = self.get_random_comp_cost(
                        index, 1, singleCost)
                    compCost = randomCost * comp['UNIT']
                else:
                    # singleCost = 0
                    compCost = 0

            if ds == 2:
                if point[0] < pds[0]:
                    singleCost = self.cal_interp(index, 1)
                    randomCost = self.get_random_comp_cost(
                        index, 1, singleCost)
                    compCost = randomCost * comp['UNIT']

                elif (point[0] >= pds[0]) and (point[0] < pds[1]):
                    singleCost = self.cal_interp(index, 2)
                    randomCost = self.get_random_comp_cost(
                        index, 2, singleCost)
                    compCost = randomCost * comp['UNIT']

                else:
                    # print(1)
                    # singleCost = 0
                    compCost = 0

            if ds == 3:
                if point[0] < pds[0]:
                    singleCost = self.cal_interp(index, 1)
                    randomCost = self.get_random_comp_cost(
                        index, 1, singleCost)
                    compCost = randomCost * comp['UNIT']

                elif (point[0] >= pds[0]) and (point[0] < pds[1]):
                    singleCost = self.cal_interp(index, 2)
                    randomCost = self.get_random_comp_cost(
                        index, 2, singleCost)
                    compCost = randomCost * comp['UNIT']

                elif (point[0] >= pds[1]) and (point[0] < pds[2]):
                    singleCost = self.cal_interp(index, 3)
                    randomCost = self.get_random_comp_cost(
                        index, 3, singleCost)
                    compCost = randomCost * comp['UNIT']
                else:
                    compCost = 0
        else:
            compCost = 0
        return compCost

    # 输入IDR 和 PFA 向量，此处应该有问题，PFA有四个，需考虑一下
    # 输出此Realization下的IDR 和 PFA
    def cal_repair(self, IDR, PFA):

        sCompCostList = np.zeros(3)
        nCompCostList = np.zeros(3)
        cCompCostList = np.zeros(3)
        storyCostList = np.zeros(3)
        #                   1 2 3
        for floor in range(1, 4):  # 层 迭代

            # if floor == 0:
            #     edp_pfa = PFA[floor - 1]
            # else:
            #     edp_pidr = IDR[floor - 1]
            #     edp_pfa = PFA[floor - 1]

            # ‘CT’ 为 PID 的构件：可以有三种 1，2，3
            #         PFA 的构件：可以有四种， 1，2，3，4
            # single floor repair cost
            sCompCost = 0
            nCompCost = 0
            cCompCost = 0
            storyCost = 0

            for n in range(1, len(self.componentData) + 1):  # 构件迭代

                # PID 构件
                if self.componentData['%s' % n]['EDP'] == 'PID':
                    edp_pidr = IDR[floor - 1]
                    compCost = self.cal_comp_repair(floor, edp_pidr, n)
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
                    compCostl = self.cal_comp_repair(floor - 1, edp_pfal,
                                                     n)  # 依据底部加速度的构件
                    compCostu = self.cal_comp_repair(floor, edp_pfau, n)
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

        frameCost = sum(storyCostList)
        sframeCost = sum(sCompCostList)
        nframeCost = sum(nCompCostList)
        cframeCost = sum(cCompCostList)

        return frameCost, sframeCost, nframeCost, cframeCost

    # 进度监控
    def progress(total_time, current_time=0, width=30):
        per = current_time / total_time * 100
        left = round(width * current_time / total_time)
        right = width - left
        if per < 100:
            print('\rProgress:[',
                  '▉' * left,
                  ' ' * right,
                  ']',
                  f' {per:.2f}%',
                  sep='',
                  end='',
                  flush=True)
        else:
            print('\rProgress:[',
                  '▉' * left,
                  ' ' * right,
                  ']',
                  f' {per:.2f}%\n',
                  sep='',
                  end='',
                  flush=True)