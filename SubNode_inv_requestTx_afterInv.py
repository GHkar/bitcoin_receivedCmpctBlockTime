## inv 메시지로 전달받은 트랜잭션 중 요청한 트랜잭션의 아이디 찾기

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


# 해당하는 트랜잭션이 있는지 찾기
def find_inv():
    global collection_inv
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_inv.find({})
    
    i = 0
    # 모든 트랜잭션의 정보를 찾음
    while i < 170:
        now_inv = take_data[i]
        next_inv = take_data[i+1]
        i = i+1
        if now_inv["requestTxCount"] > 0 :
            requestTxList = now_inv["requestTx"]
            invTxList = next_inv["inv_list"]
            for tx in requestTxList:
                for inv in invTxList:
                    tx_list = inv["acceptMempoolTx"]
                    for it in tx_list:
                        if tx["txid"] == it:
                            print("exist block = " + str(now_inv["_id"]) + ", tx = " + str(tx["txid"]))



if __name__ == '__main__':
    connect_mongoDB()
    find_inv()
