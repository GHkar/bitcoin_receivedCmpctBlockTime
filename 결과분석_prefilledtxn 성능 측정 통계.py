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


# 몽고 db 연결
def connect_mongoDB():
    global collection_1
    global collection_2
    global collection_3

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["1check_performance_per_phase"]
    collection_2 = mydb["2check_performance_per_phase"]
    collection_3 = mydb["3check_performance_per_phase"]



# 통계 내기
def calculate_receivedTime_statistic():
    global collection_1
    global collection_2
    global collection_3

    take_data1 = collection_1.find({})
    take_data2 = collection_2.find({})
    take_data3 = collection_3.find({})

    # 요청한 트랜잭션 reqeust
    # preparing = []
    # readingMempool = []
    # indexing = []
    # ordering = []
    # fillingprefilled = []
    # orderingindex = []
    # changeindex = []
    # makingshortids = []

    info1 = []
    info2 = []
    info3 = []

    # 모든 트랜잭션의 정보를 찾음
    for td in take_data1:
        #if float(td["preparing"]) > 0:
        info1.append(float(td["preparing"]))

    for td in take_data2:
        #if float(td["preparing"]) > 0:
        info2.append(float(td["preparing"]))

    for td in take_data3:
        #if float(td["preparing"]) > 0:
        info3.append(float(td["preparing"]))

    # 평균 시간
    print("평균시간1")
    print(format(np.average(info1),'.20f'))
    print("평균시간2")
    print(format(np.average(info2),'.20f'))
    print("평균시간3")
    print(format(np.average(info3),'.20f'))

    print("전체 평균")
    print(format((np.average(info1) + np.average(info2) + np.average(info3))/3, '.20f'))



if __name__ == '__main__':
    connect_mongoDB()
    calculate_receivedTime_statistic()
