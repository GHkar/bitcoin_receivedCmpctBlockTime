## prefilledtxn 블록 사이즈 증가 비교 수집 통계

import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from matplotlib import pyplot as plt

# 변수 선언
# 콜렉션
collection_1 = []
collection_2 = []
collection_3 = []
collection_4 = []
collection_5 = []
collection_6 = []
collection_7 = []

# 몽고 db 연결
def connect_mongoDB():
    global collection_1
    global collection_2
    global collection_3
    global collection_4
    global collection_5
    global collection_6
    global collection_7

    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["50-1Blocksize"]
    collection_2 = mydb["50-2Blocksize"]
    collection_3 = mydb["50-3Blocksize"]
    collection_4 = mydb["50-4Blocksize"]
    collection_5 = mydb["pb30-Blocksize"]
    collection_6 = mydb["pb40-Blocksize"]
    collection_7 = mydb["pbm-Blocksize"]



# 통계 내기
def calculate_size_fee_statistic():
    global collection_1
    global collection_2
    global collection_3
    global collection_4
    global collection_5
    global collection_6
    global collection_7

    # {"$gt":682075} {"$lt":681905}
    take_data1 = collection_1.find({})
    take_data2 = collection_2.find({})
    take_data3 = collection_3.find({})
    take_data4 = collection_4.find({})
    take_data5 = collection_5.find({})
    take_data6 = collection_6.find({})
    take_data7 = collection_7.find({})

    # 요청한 트랜잭션 reqeust
    bSize1 = []
    bSize2 = []
    bSize3 = []
    bSize4 = []
    bSize5 = []
    bSize6 = []
    bSize7 = []

    # 모든 트랜잭션의 정보를 찾음
    for td in take_data1:
        bSize1.append(td["size"])

    for td in take_data2:
        bSize2.append(td["size"])

    for td in take_data3:
        bSize3.append(td["size"])

    for td in take_data4:
        bSize4.append(td["size"])

    for td in take_data5:
        bSize5.append(td["size"])

    for td in take_data6:
        bSize6.append(td["size"])

    for td in take_data7:
        bSize7.append(td["size"])



    print("평균 사이즈 1")
    print(np.average(bSize1))
    print("평균 사이즈 2")
    print(np.average(bSize2))
    print("평균 사이즈 3")
    print(np.average(bSize3))
    print("평균 사이즈 4")
    print(np.average(bSize4))
    print("평균 사이즈 5")
    print(np.average(bSize5))
    print("평균 사이즈 6")
    print(np.average(bSize6))
    print("평균 사이즈 7")
    print(np.average(bSize7))




if __name__ == '__main__':
    connect_mongoDB()
    calculate_size_fee_statistic()
