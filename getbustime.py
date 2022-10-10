import time
import numpy
import requests
import json
import pandas as pd
import numpy as np
import transform

# import jsonpath

ODFlow = []
records = []
errecords = []
config_dir = 'E:/实验/研究方向/python/计算结果/研究区1晚高峰'
error_dir = 'E:/实验/研究方向/python/计算结果/error_研究区1晚高峰'
num = 0


def get_time():
    global num
    with open('E:/实验/研究方向/python/火星坐标/研究区1晚高峰.csv', 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.strip('\n')
            if line != None:
                ot, dt, start, ogrid, ox, oy, dgrid, dx, dy, olon, olat, dlon, dlat, total = line.split(',')
                # flow = [olon, olat, dlon, dlat]
                # omglon, omglat, dmglon, dmglat = transform.tranlate(flow)
                # WGS84转化为火星坐标
                ori = str(olon) + ',' + str(olat)
                des = str(dlon) + ',' + str(dlat)
                bus_result = get_bus_result(ori, des, start)
                bus_info = json.loads(bus_result)
                bus_code = bus_info['status']
                if int(bus_code) == 0:
                    errmsg = str(line)
                    errecords.append(errmsg)
                    write_errorfile(error_dir + '.csv')
                    continue
                else:
                    bus_distance, bustime, walking_distance = get_bustime(bus_info)
                    # bustime == ('%.3f' % bustime)

                    # 抓取驾车规划所需时间
                    car_result = get_car_result(ori, des)
                    car_info = json.loads(car_result)
                    car_code = car_info['status']
                    if int(car_code) == 0:
                        errmsg = str(line)
                        errecords.append(errmsg)
                        write_errorfile(error_dir + '.csv')
                        continue
                    else:
                        car_distance, cartime = get_cartime(car_info)
                        # cartime = ('%.3f' % cartime)
                        K = float(bustime) / float(cartime)
                        K = ('%.3f' % K)
                        # 计算公交竞争指数
                        # time.sleep(1)
                        # msg = str(ot) + ',' + str(dt) + ',' + str(start) + ',' + str(ogrid) + ',' + str(ox) + ',' + str(
                        #     oy) + ',' + str(dgrid) + ',' + str(dx) + ',' + str(dy) + ',' + str(total) + ',' + str(
                        #     bus_distance) + ',' + str(bustime) + ',' + str(walking_distance) + ',' + str(
                        #     car_distance) + ',' + str(cartime) + ',' + str(K)
                        msg = str(line) + ',' + str(bus_distance) + ',' + str(bustime) + ',' + str(
                            walking_distance) + ',' + str(car_distance) + ',' + str(cartime) + ',' + str(K)
                        records.append(msg)
                        # print(records)
                        write_file(config_dir + '.csv')
                        num = num + 1
                        if num % 200 == 0:
                            print(num)
                # time.sleep(1)
            else:
                print("读取数据结束了！")
        write_file(config_dir + '.csv')


def get_bus_result(ori, des, start):
    url = "https://restapi.amap.com/v3/direction/transit/integrated?parameters"
    myParams = {
        "origin": ori,
        "destination": des,
        "strategy": "0",
        "city": "beijing",
        "output": "json",
        "key": "a050451db36ff9811651a9f2a30a2099",
        "time": start
    }
    while True:
        try:
            bus_res = requests.get(url=url, params=myParams, headers={'Connection': 'close'}, timeout=(50, 100))
            break
        except:
            time.sleep(2)
            continue
    if bus_res.status_code != 200:
        print("调用失败")
    else:
        bus_text = bus_res.text
        return bus_text


# 请求汽车出行数据
def get_car_result(ori, des):
    url = "https://restapi.amap.com/v3/direction/driving?parameters"
    myParams = {
        "origin": ori,
        "destination": des,
        "output": "json",
        "key": "a050451db36ff9811651a9f2a30a2099",
    }
    while True:
        try:
            car_res = requests.get(url=url, params=myParams, headers={'Connection': 'close'}, timeout=(50, 100))
            break
        except:
            time.sleep(2)
            continue
    if car_res.status_code != 200:
        print("调用失败")
    else:
        car_text = car_res.text
        return car_text


def get_bustime(info):
    if info["info"] == 'OK':
        try:
            distance = info['route']['distance']  # 起点到终点的步行距离
        except:
            distance = 0
        try:
            bustime = info['route']['transits'][0]['duration']
            # bustime = float(bustime) / 3600
            walking_distance = info['route']['transits'][0]['walking_distance']
        except:
            bustime = 0
            walking_distance = 0
        return distance, bustime, walking_distance;
    else:
        print("出错了!")


def get_cartime(info):
    if info["info"] == 'OK':
        try:
            car_distance = info["route"]["paths"][0]['distance']
            cartime = info["route"]["paths"][0]["duration"]
            # cartime = float(cartime) / 3600
        except:
            car_distance = 0
            cartime = 0
        return car_distance, cartime;
    else:
        print("数据提取出错了！")


def write_file(filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for r in records:
            f.write(r + '\n')
        records.clear()


def write_errorfile(errorfilename):
    with open(errorfilename, 'a', encoding='utf-8') as f:
        for r in errecords:
            f.write(r + '\n')
        errecords.clear()


if __name__ == '__main__':
    get_time()
