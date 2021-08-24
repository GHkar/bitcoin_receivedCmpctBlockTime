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


# 몽고 db 연결
def connect_mongoDB():
    global collection_1

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["nTx"]



# 통계 내기
def calculate_ntx():
    global collection_1
    # {"$gt":682075} {"$lt":681905}
    take_data1 = collection_1.find({})

    # 트랜잭션 개수
    ntx = []


    # 모든 트랜잭션의 정보를 찾음
    for td in take_data1:
        ntx.append(td["ntx"])

    # 평균 시간
    print("평균개수")
    print(np.average(ntx))



if __name__ == '__main__':
    connect_mongoDB()
    calculate_ntx()
