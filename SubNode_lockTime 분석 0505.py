## 요청한 트랜잭션과 요청하지 않은 트랜잭션 fee와 size 추가 통계 0505-0506

import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from matplotlib import pyplot as plt

# 변수 선언
# 콜렉션
collection_txFeeSize = []
collection_rtx = []


# 몽고 db 연결
def connect_mongoDB():
    global collection_txFeeSize
    global collection_rtx

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection_txFeeSize = mydb["SubNode_0506BlocksTx"]
    collection_rtx = mydb["log_SubNode_rtx_0506"]

    # 0420 = SubNode_0420BlocksTx_fee, SubNode_requestTx_locktime
    # 0505 = SubNode_0505BlocksTx_fee, log_SubNode_received_Inv
    # 0506 = SubNode_0506BlocksTx_fee, log_SubNode_rtx_0506


# 요청한 트랜잭션 리스트 만들기
def find_request_Tx(collection):
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection.find({})
    rtx_list = []
    for td in take_data:
        for t in td["requestTx"]:
            rtx_list.append(t["txid"])

    return rtx_list

# 통계 내기
def calculate_size_fee_statistic():
    global collection_txFeeSize
    global collection_rtx

    rtx_list = find_request_Tx(collection_rtx)
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_txFeeSize.find({})

    # 요청한 트랜잭션 reqeust
    rtx_locktime = []
    # 요청하지 않은 트랜잭션 unrequest
    utx_locktime = []

    # locktime 저장
    for tx in take_data:
        if tx["_id"] in rtx_list :
            rtx_locktime.append(tx["locktime"])
        else :
            utx_locktime.append(tx["locktime"])
    

    rc = 0
    uc = 0

    for rt in rtx_locktime:
        if rt == 0 :
            rc = rc + 1

    for ut in utx_locktime:
        if ut == 0 :
            uc = uc + 1

    print(rc/len(rtx_locktime))
    print(uc/len(utx_locktime))


    



if __name__ == '__main__':
    connect_mongoDB()
    calculate_size_fee_statistic()
