import json
import math
import numpy as np

# from transbigdata.coordinates import transformlat, transformlng

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率
records = []
num = 0
config_dir = 'G:/实验/研究方向/python/火星坐标/研究区6晚高峰'


def tranlate():
    global num
    with open('G:/实验/研究方向/python/WGS84坐标/研究区6晚高峰.csv', 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.strip('\n')
            if line != None:
                ot, dt, start, ogrid, ox, oy, dgrid, dx, dy, olon, olat, dlon, dlat, total = line.split(',')
                omglon, omglat = wgs84togcj02(olon, olat)
                dmglon, dmglat = wgs84togcj02(dlon, dlat)
                msg = str(ot) + ',' + str(dt) + ',' + str(start) + ',' + str(ogrid) + ',' + str(ox) + ',' + str(
                    oy) + ',' + str(dgrid) + ',' + str(dx) + ',' + str(dy) + ',' + str(omglon) + ',' + str(
                    omglat) + ',' + str(dmglon) + ',' + str(dmglat) + ',' + str(total)
                records.append(msg)
                num = num + 1
                write_file(config_dir + '.csv')
                if num % 500 == 0:
                    print(num)
                # write_file(config_dir + '.csv')

    # else:
    # print("出错了")


def wgs84togcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    lng = float(lng)
    lat = float(lat)
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    mglat = ('%.5f' % mglat)
    mglng = ('%.5f' % mglng)
    return str(mglng), str(mglat)


def gcj02towgs84(lng, lat):
    """"
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系的纬度
    :return:
    """
    lng = float(lng)
    lat = float(lat)
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def write_file(filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for r in records:
            f.write(r + '\n')
        records.clear()


if __name__ == '__main__':
    tranlate()
