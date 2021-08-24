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


# 몽고 db 연결
def connect_mongoDB():
    global collection_1
    global collection_2
    global collection_3
    global collection_4

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.29.228:80/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["premise_requestTxn_1"]
    collection_2 = mydb["premise_requestTxn_2"]
    collection_3 = mydb["premise_requestTxn_3"]
    collection_4 = mydb["premise_requestTxn_4"]



# 통계 내기
def calculate_size_fee_statistic():
    global collection_1
    global collection_2
    global collection_3
    global collection_4
    # {"$gt":682075} {"$lt":681905}
    take_data1 = collection_1.find({})
    take_data2 = collection_2.find({})
    take_data3 = collection_3.find({})
    take_data4 = collection_4.find({})

    # 요청한 트랜잭션 reqeust
    rtx1 = []
    rtx2 = []
    rtx3 = []
    rtx4 = []

    i = 0
    total_block = 115
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


    print("요청확률1")
    print(len(rtx1)/total_block)
    print("요청확률2")
    print(len(rtx2)/total_block)
    print("요청확률3")
    print(len(rtx3)/total_block)
    print("요청확률4")
    print(len(rtx4)/total_block)

    print("평균개수1")
    print(np.average(rtx1))
    print("평균개수2")
    print(np.average(rtx2))
    print("평균개수3")
    print(np.average(rtx3))
    print("평균개수4")
    print(np.average(rtx4))

    print("사분위수1")
    print(np.quantile(rtx1,[0.25,0.5,0.75]))
    print("사분위수2")
    print(np.quantile(rtx2,[0.25,0.5,0.75]))
    print("사분위수3")
    print(np.quantile(rtx3,[0.25,0.5,0.75]))
    print("사분위수4")
    print(np.quantile(rtx4,[0.25,0.5,0.75]))





if __name__ == '__main__':
    connect_mongoDB()
    calculate_size_fee_statistic()
