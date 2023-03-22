## inv 메시지 내에서 요청된 트랜잭션과 요청되지 않은 트랜잭션의 개수 세기

import pymongo
from pymongo import MongoClient
import time
import datetime
import numpy as np

# 변수 선언
# 콜렉션
collection_inv = []


# 몽고 db 연결
def connect_mongoDB():
    global collection_inv

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection_inv = mydb["log_SubNode_received_Inv"]


# inv 메시지 카운트 세기
def count_inv():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({})
    
    inv_count = []
    # 모든 트랜잭션의 정보를 찾음
    for inv in take_data:
        inv_count.append(inv["invCount"])

    print(np.average(inv_count))
    print(np.max(inv_count))
    print(np.min(inv_count))

def count_inv_request():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({"requestTxCount" : {"$gt" : 0}})
    
    inv_count = []
    # 모든 트랜잭션의 정보를 찾음
    for inv in take_data:
        inv_count.append(inv["invCount"])

    print(np.average(inv_count))
    print(np.max(inv_count))
    print(np.min(inv_count))

def count_inv_Unrequest():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({"requestTxCount" : {"$eq" : 0}})
    
    inv_count = []
    # 모든 트랜잭션의 정보를 찾음
    for inv in take_data:
        inv_count.append(inv["invCount"])

    print(np.average(inv_count))
    print(np.max(inv_count))
    print(np.min(inv_count))

if __name__ == '__main__':
    connect_mongoDB()
    count_inv()
    count_inv_request()
    count_inv_Unrequest()
