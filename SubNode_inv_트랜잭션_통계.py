## inv 메시지 개수 비교하기
# 전체, 요청한 것, 안한 것

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
    
    tx_count = []
    # 모든 트랜잭션의 정보를 찾음
    for block in take_data:
        one = block["inv_list"]
        for inv in one:
            tx_count.append(inv["txCount"])

    print(np.average(tx_count))
    print(np.max(tx_count))
    print(np.min(tx_count))

def count_inv_request():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({"requestTxCount" : {"$gt" : 0}})
    
    tx_count = []
    # 모든 트랜잭션의 정보를 찾음
    for block in take_data:
        one = block["inv_list"]
        for inv in one:
            tx_count.append(inv["txCount"])

    print(np.average(tx_count))
    print(np.max(tx_count))
    print(np.min(tx_count))

def count_inv_Unrequest():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({"requestTxCount" : {"$eq" : 0}})
    
    tx_count = []
    # 모든 트랜잭션의 정보를 찾음
    for block in take_data:
        one = block["inv_list"]
        for inv in one:
            tx_count.append(inv["txCount"])

    print(np.average(tx_count))
    print(np.max(tx_count))
    print(np.min(tx_count))

if __name__ == '__main__':
    connect_mongoDB()
    count_inv()
    count_inv_request()
    count_inv_Unrequest()
