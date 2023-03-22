## 자카드 지수 분석
# 전체, 요청한 것, 안한 것

import pymongo
from pymongo import MongoClient
import time
import datetime
import numpy as np

# 변수 선언
# 콜렉션
collection_inv = []
collection_rtx = []


# 몽고 db 연결
def connect_mongoDB():
    global collection_inv
    global collection_rtx

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection_inv = mydb["log_MainNode_inv_JaccardIndex"]
    collection_rtx = mydb["log_MainNode_peer_requestTx"]


# inv 메시지 카운트 세기
def count_inv():
    global collection_inv
    
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({})
    
    tx_count = []
    # 모든 트랜잭션의 정보를 찾음
    for block in take_data:
        tx_count.append(block["inv_jaccard"])

    print(np.average(tx_count))
    print(np.max(tx_count))
    print(np.min(tx_count))

def count_inv_request():
    global collection_inv
    global collection_rtx
    tx_count = []

     # 트랜잭션을 요청한 블록을 불러 옴
    td = collection_rtx.find({"requestTxCount" : {"$gt" : 0}})
    for t in td:
        take_data = collection_inv.find_one({"_id" : t["_id"]})
        tx_count.append(take_data["inv_jaccard"])
    
       

    print(np.average(tx_count))
    print(np.max(tx_count))
    print(np.min(tx_count))

def count_inv_Unrequest():
    global collection_inv
    global collection_rtx
    tx_count = []

     # 트랜잭션을 요청하지  블록을 불러 옴
    td = collection_rtx.find({"requestTxCount" : {"$eq" : 0}})
    for t in td:
        take_data = collection_inv.find_one({"_id" : t["_id"]})
        tx_count.append(take_data["inv_jaccard"])
    

    print(np.average(tx_count))
    print(np.max(tx_count))
    print(np.min(tx_count))

if __name__ == '__main__':
    connect_mongoDB()
    count_inv()
    count_inv_request()
    count_inv_Unrequest()
