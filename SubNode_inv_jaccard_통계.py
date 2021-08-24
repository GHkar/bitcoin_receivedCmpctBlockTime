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
    collection_inv = mydb["log_SubNode_inv_block_Tx_jaccardIndex"]


def count_inv_request():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({"requestTxCount" : {"$gt" : 0}, "blockTxCount" : {"$gt" : 2500, "$lt" : 3000}})
    
    tx_count1 = []
    tx_count2 = []
    tx_count3 = []
    tx_count4 = []
    # 모든 트랜잭션의 정보를 찾음
    for block in take_data:
        tx_count1.append(block["inv_block_tx_jaccard"])
        tx_count2.append(block["inter/block"])
        tx_count3.append(block["invTxCount"])
        tx_count4.append(block["invCount"])

    print("트랜잭션 요청 안 함")
    print("자카드")
    print(np.average(tx_count1))
    print(np.max(tx_count1))
    print(np.min(tx_count1))

    print("블록")
    print(np.average(tx_count2))
    print(np.max(tx_count2))
    print(np.min(tx_count2))

    print("inv Tx")
    print(np.average(tx_count3))
    print(np.max(tx_count3))
    print(np.min(tx_count3))

    print("inv num")
    print(np.average(tx_count4))
    print(np.max(tx_count4))
    print(np.min(tx_count4))

def count_inv_Unrequest():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({"requestTxCount" : {"$eq" : 0}, "blockTxCount" : {"$gt" : 2500, "$lt" : 3000} })
    
    tx_count1 = []
    tx_count2 = []
    tx_count3 = []
    tx_count4 = []
    # 모든 트랜잭션의 정보를 찾음
    for block in take_data:
        tx_count1.append(block["inv_block_tx_jaccard"])
        tx_count2.append(block["inter/block"])
        tx_count3.append(block["invTxCount"])
        tx_count4.append(block["invCount"])

    print("트랜잭션 요청 안 함")
    print("자카드")
    print(np.average(tx_count1))
    print(np.max(tx_count1))
    print(np.min(tx_count1))

    print("블록")
    print(np.average(tx_count2))
    print(np.max(tx_count2))
    print(np.min(tx_count2))

    print("inv Tx")
    print(np.average(tx_count3))
    print(np.max(tx_count3))
    print(np.min(tx_count3))

    print("inv num")
    print(np.average(tx_count4))
    print(np.max(tx_count4))
    print(np.min(tx_count4))

if __name__ == '__main__':
    connect_mongoDB()
    count_inv_request()
    count_inv_Unrequest()
