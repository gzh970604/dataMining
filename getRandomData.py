import pandas as pd
from pyproj import Proj
from pyproj import Transformer
import numpy as np

ODFlow = []
data_file = 'G:/实验/研究方向/python/WGS84坐标/研究区6晚高峰'


# G:/实验/研究方向/python/WGS84坐标/flow8
# 生成网格内随机数据并转换为WGS84坐标
def get_point():
    # global ODFlow
    with open('G:/实验/研究方向/研究区/人口通量_研究区/研究区6晚高峰数据.csv', 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.strip('\n')
            if line != None:
                ot, dt, ogrid, ogridx, ogridy, dgrid, dgridx, dgridy, total, dis = line.split(',')
                for i in range(0, int(total)):
                    start = np.random.rand() * (int(dt) - int(ot)) + int(ot)
                    start = ('%.4f' % start)
                    ox = np.random.rand() * 500.0 - 250.0 + float(ogridx)
                    oy = np.random.rand() * 500.0 - 250.0 + float(ogridy)
                    dx = np.random.rand() * 500.0 - 250.0 + float(dgridx)
                    dy = np.random.rand() * 500.0 - 250.0 + float(dgridy)
                    # ogridlon, ogridlat = get_WGS84(ogridx, ogridy)
                    # dgridlon, dgridlat = get_WGS84(dgridx, dgridy)
                    olon, olat = get_WGS84(ox, oy)
                    dlon, dlat = get_WGS84(dx, dy)
                    flow = str(ot) + ',' + str(dt) + ',' + str(start) + ',' + str(ogrid) + ',' + str(
                        ogridx) + ',' + str(ogridy) + ',' + str(dgrid) + ',' + str(dgridx) + ',' + str(
                        dgridy) + ',' + str(olon) + ',' + str(olat) + ',' + str(dlon) + ',' + str(dlat) + ',' + str(
                        total)
                    ODFlow.append(flow)
            write_datafile(data_file + '.csv')


# 生成网格的顶点坐标
def get_grid():
    # global ODFlow
    with open('G:/实验/研究方向/python/test.csv', 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.strip('\n')
            if line != None:
                ot, dt, ogrid, ogridx, ogridy, dgrid, dgridx, dgridy, num, total, NII = line.split(',')
                olon, olat = get_WGS84(ogridx, ogridy)
                dlon, dlat = get_WGS84(dgridx, dgridy)
                odwkt = "LINESTRING(" + str(olon) + " " + str(olat) + "," + str(dlon) + " " + str(dlat) + ")"
                msg = [ot, dt, ogrid, olon, olat, dgrid, dlon, dlat, num, total, NII]
                # msg = str(ot) + ',' + str(dt) + ',' + str(ogrid) + ',' + str(olon) + ',' + str(olat) + ',' + str(
                #     dgrid) + ',' + str(dlon) + ',' + str(dlat) + ',' + str(total)
                ODFlow.append(msg)
        df = pd.DataFrame(ODFlow, columns=['1', '2', '3', 'olon', 'olat', '6', 'dlon', 'dlat', '9', '10', '11'])
        df['odwkt'] = df.apply(mkod, axis=1)
        df.to_csv(r"test_viz.csv", index=False, header=False, sep=",")


def mkod(r):
    odwkt = "LINESTRING(" + str(r.olon) + " " + str(r.olat) + "," + str(r.dlon) + " " + str(r.dlat) + ")"
    return odwkt


# def grid():
#     # global ODFlow
#     with open('研究区.csv', 'r', encoding='utf-8') as f:
#         for lines in f.readlines():
#             line = lines.strip('\n')
#             if line != None:
#                 ot, dt, ogrid, ogridx, ogridy, dgrid, dgridx, dgridy, num, total = line.split(',')
#                 x1 = float(x) + 250.0
#                 x2 = float(x) - 250.0
#                 y1 = float(y) + 250.0
#                 y2 = float(y) - 250.0
#                 lon1, lat1 = get_WGS84(x2, y1)
#                 lon2, lat2 = get_WGS84(x1, y1)
#                 lon3, lat3 = get_WGS84(x1, y2)
#                 lon4, lat4 = get_WGS84(x2, y2)
#                 msg = str(ot) + ',' + str(dt) + ',' + str(ogrid) + ',' + str(olon) + ',' + str(olat) + ',' + str(
#                     dgrid) + ',' + str(dlon) + ',' + str(dlat) + ',' + str(total)
#                 ODFlow.append(msg)
#         write_datafile(data_file + '.csv')


def get_WGS84(X, Y):
    proj1 = Proj("epsg:32650")
    lon, lat = proj1(X, Y, inverse=True)
    lon = ('%.5f' % lon)
    lat = ('%.5f' % lat)
    return lon, lat;


# def get_projection():
#     with open('start9.csv', 'r', encoding='utf-8') as f:
#         for lines in f.readlines():
#             line = lines.strip('\n')
#             if line != None:
#                 ot, start, ogrid, olon, olat, dt, dgrid, dlon, dlat, total = line.split(',')
#                 ox, oy = get_WGS84(olon, olat)
#                 dx, dy = get_WGS84(dlon, dlat)
#
# def get_UIM(lon, lat):
#     transformer = Transformer.from_crs("epsg:4326", "epsg:32650")
#     x, y = transformer.transform(lat, lon)
#     return x, y;


def write_datafile(filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for r in ODFlow:
            f.write(r + '\n')
        ODFlow.clear()


if __name__ == '__main__':
    get_point()
    # get_grid()
