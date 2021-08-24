## 요청한 트랜잭션과 요청하지 않은 트랜잭션 fee와 size 추가 통계 0505-0506

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

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["50-1requestTxn"]
    collection_2 = mydb["50-2requestTxn"]
    collection_3 = mydb["50-3requestTxn"]
    collection_4 = mydb["50-4requestTxn"]
    collection_5 = mydb["pb30-requestTxn"]
    collection_6 = mydb["pb40-requestTxn"]
    collection_7 = mydb["pbm-requestTxn"]



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

    # take_data1 = collection_1.find({"_id":{"$lte":691108}})
    # take_data2 = collection_2.find({"_id":{"$lte":691108}})
    # take_data3 = collection_3.find({"_id":{"$lte":691108}})
    # take_data4 = collection_4.find({"_id":{"$lte":691108}})

    # 요청한 트랜잭션 reqeust
    rtx1 = []
    rtx2 = []
    rtx3 = []
    rtx4 = []
    rtx5 = []
    rtx6 = []
    rtx7 = []

    i = 0
    total_block = 327
    # 모든 트랜잭션의 정보를 찾음
    for td in take_data1:
        if td["requestTx"] != 0 :
            rtx1.append(td["requestTx"])

    for td in take_data2:
        if td["requestTx"] != 0 :
            rtx2.append(td["requestTx"])

    for td in take_data3:
        if td["requestTx"] != 0 :
            rtx3.append(td["requestTx"])

    for td in take_data4:
        if td["requestTx"] != 0 :
            rtx4.append(td["requestTx"])

    for td in take_data5:
        if td["requestTx"] != 0 :
            rtx5.append(td["requestTx"])

    for td in take_data6:
        if td["requestTx"] != 0 :
            rtx6.append(td["requestTx"])

    for td in take_data7:
        if td["requestTx"] != 0 :
            rtx7.append(td["requestTx"])


    print("요청확률1")
    print(len(rtx1)/total_block)
    print("요청확률2")
    print(len(rtx2)/total_block)
    print("요청확률3")
    print(len(rtx3)/total_block)
    print("요청확률4")
    print(len(rtx4)/total_block)
    print("요청확률5")
    print(len(rtx5)/total_block)
    print("요청확률6")
    print(len(rtx6)/total_block)
    print("요청확률7")
    print(len(rtx7)/total_block)

    print("평균개수1")
    print(np.average(rtx1))
    print("평균개수2")
    print(np.average(rtx2))
    print("평균개수3")
    print(np.average(rtx3))
    print("평균개수4")
    print(np.average(rtx4))
    print("평균개수5")
    print(np.average(rtx5))
    print("평균개수6")
    print(np.average(rtx6))
    print("평균개수7")
    print(np.average(rtx7))








if __name__ == '__main__':
    connect_mongoDB()
    calculate_size_fee_statistic()
