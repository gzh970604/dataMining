import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

num = 1  # 低效流的数目
total = 1  # 流的总数
records = []
config_dir = 'test'
C = 0

MinNII = 0.6


# def CLIQUE(data):
#     data = np.array(data)
#     for i in range(len(data)):
#         if data[i, 4] >= MinNII:
#             C = C + 1
#             data[i, 5] = C


# def ExpandCluster(C):
#
# def RegionQury():
#     D=max(pdist2())


def get_gridNII():
    global num, total, R
    with open('G:/实验/研究方向/python/计算结果/研究区1数据.csv', 'r', encoding='utf-8') as f:
        data = np.loadtxt(f, float, delimiter=",", skiprows=0)
    data = np.array(data)
    # df=pd.DataFrame(flow)
    data = data[np.lexsort(data.T[3, None])]
    df = pd.DataFrame(data,
                      columns=['ot', 'dt', 'start', 'ogrid', 'ox', 'oy', 'dgrid', 'dx', 'dy', 'olon', 'olat', 'dlon',
                               'dlat', 'total', 'distance', 'bustime', 'walkdistance', 'cardistance', 'cartime', 'K'])
    df.drop(df.index[(df['K'] == 0)], inplace=True)
    flow = df.values
    # 类型转换
    # print(flow[:, 1:3])
    NII = flow[:, 19]
    R = np.average(NII, axis=0)
    print(R)
    for i in range(len(flow) - 1):
        if flow[i, 3] == flow[i + 1, 3] and flow[i, 6] == flow[i + 1, 6]:
            if flow[i, 19] > R:
                num = num + 1
                total = total + 1
            else:
                total = total + 1
        else:
            NII = num / total
            NII = ('%.3f' % NII)
            msg = str(flow[i, 0]) + ',' + str(flow[i, 1]) + ',' + str(flow[i, 3]) + ',' + str(flow[i, 4]) + ',' + str(
                flow[i, 5]) + ',' + str(flow[i, 6]) + ',' + str(flow[i, 7]) + ',' + str(flow[i, 8]) + ',' + str(
                num) + ',' + str(total) + ',' + str(NII)
            records.append(msg)
            num = 1
            total = 1
    NII = num / total
    NII = ('%.3f' % NII)
    msg = str(flow[i, 0]) + ',' + str(flow[i, 1]) + ',' + str(flow[i, 3]) + ',' + str(flow[i, 4]) + ',' + str(
        flow[i, 5]) + ',' + str(flow[i, 6]) + ',' + str(flow[i, 7]) + ',' + str(flow[i, 8]) + ',' + str(
        num) + ',' + str(total) + ',' + str(NII)
    records.append(msg)
    write_file(config_dir + '.csv')


def write_file(filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for r in records:
            f.write(r + '\n')
        records.clear()


if __name__ == '__main__':
    get_gridNII()
