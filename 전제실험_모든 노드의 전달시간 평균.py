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
    mydb = myclient['bitcoin']
    collection_1 = mydb["log_SubNode_cmpctblock_received_time_per_height"]
    collection_2 = mydb["log_SubNode_cmpctblock_received_time_per_height2"]
    collection_3 = mydb["log_SubNode_cmpctblock_received_time_per_height3"]
    collection_4 = mydb["log_SubNode_cmpctblock_received_time_per_height4"]



# 통계 내기
def calculate_receivedTime_statistic():
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
    receivedTime1 = []
    receivedTime2 = []
    receivedTime3 = []
    receivedTime4 = []


    # 모든 트랜잭션의 정보를 찾음
    for td in take_data1:
        receivedTime1.append(td["receiveTime_result"])

    for td in take_data2:
        receivedTime2.append(td["receiveTime_result"])

    for td in take_data3:
        receivedTime3.append(td["receiveTime_result"])

    for td in take_data4:
        receivedTime4.append(td["receiveTime_result"])

    # 평균 시간
    print("평균시간1")
    print(np.average(receivedTime1))
    print("평균시간2")
    print(np.average(receivedTime2))
    print("평균시간3")
    print(np.average(receivedTime3))
    print("평균시간4")
    print(np.average(receivedTime4))




if __name__ == '__main__':
    connect_mongoDB()
    calculate_receivedTime_statistic()
