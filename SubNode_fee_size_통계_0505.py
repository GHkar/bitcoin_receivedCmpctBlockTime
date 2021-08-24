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
    collection_txFeeSize = mydb["SubNode_0505BlocksTx_fee"]
    collection_rtx = mydb["log_SubNode_received_Inv"]

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
    rtx_fee = []
    rtx_size = []
    # 요청하지 않은 트랜잭션 unrequest
    utx_fee = []
    utx_size = []

    # 모든 트랜잭션의 정보를 찾음
    for tx in take_data:
        if tx["_id"] in rtx_list :
            rtx_fee.append(tx["fee"])
            rtx_size.append(tx["size"])
        else :
            utx_fee.append(tx["fee"])
            utx_size.append(tx["size"])
    
    
    rf = pd.Series(rtx_fee)
    rs = pd.Series(rtx_size)
    uf = pd.Series(utx_fee)
    us = pd.Series(utx_size)

    q1 = rf.quantile(.25)
    q2 = rf.quantile(.5)
    q3 = rf.quantile(.75)

    print("요청한 트랜잭션 fee")
    print(np.average(rtx_fee))
    print(np.std(rtx_fee))
    print(format(q1, '.20f'))
    print(format(q2, '.20f'))
    print(format(q3, '.20f'))

    q1 = uf.quantile(.25)
    q2 = uf.quantile(.5)
    q3 = uf.quantile(.75)

    print("요청하지 않은 트랜잭션 fee")
    print(np.average(utx_fee))
    print(np.std(utx_fee))
    print(format(q1, '.20f'))
    print(format(q2, '.20f'))
    print(format(q3, '.20f'))

    q1 = rs.quantile(.25)
    q2 = rs.quantile(.5)
    q3 = rs.quantile(.75)

    print("요청한 트랜잭션 size")
    print(np.average(rtx_size))
    print(np.std(rtx_size))
    print(format(q1, '.20f'))
    print(format(q2, '.20f'))
    print(format(q3, '.20f'))

    q1 = us.quantile(.25)
    q2 = us.quantile(.5)
    q3 = us.quantile(.75)

    print("요청하지 않은 트랜잭션 size")
    print(np.average(utx_size))
    print(np.std(utx_size))
    print(format(q1, '.20f'))
    print(format(q2, '.20f'))
    print(format(q3, '.20f'))

    dictdata1 = {"rtx_fee":rtx_fee}
    dictdata2 = {"rtx_size":rtx_size}
    dictdata3 = {"utx_fee":utx_fee}
    dictdata4 = {"utx_size":utx_size}
    df1 = df(dictdata1)
    df2 = df(dictdata2)
    df3 = df(dictdata3)
    df4 = df(dictdata4)

    fig, ax = plt.subplots()
    plt.boxplot([df1["rtx_fee"], df3["utx_fee"]], sym="b*")
    #plt.boxplot([df2["rtx_size"], df4["utx_size"]])
    plt.title("Fee")
    plt.xticks([1,2],['rtx','utx'])
    plt.show()





if __name__ == '__main__':
    connect_mongoDB()
    calculate_size_fee_statistic()



    ### box plot 만드는 코드
    # dictdata1 = {"rtx_fee":rtx_fee}
    # dictdata2 = {"rtx_size":rtx_size}
    # dictdata3 = {"utx_fee":utx_fee}
    # dictdata4 = {"utx_size":utx_size}
    # df1 = df(dictdata1)
    # df2 = df(dictdata2)
    # df3 = df(dictdata3)
    # df4 = df(dictdata4)

    # fig, ax = plt.subplots()
    # plt.boxplot([df1["rtx_fee"], df3["utx_fee"]], sym="b*")
    # #plt.boxplot([df2["rtx_size"], df4["utx_size"]], sym="b*")
    # plt.title("Fee")
    # plt.xticks([1,2],['rtx','utx'])
    # plt.show()



    ### 통계
    # print("요청한 트랜잭션 fee")
    # print(np.average(rtx_fee))
    # print(np.max(rtx_fee))
    # print(np.min(rtx_fee))

    # print("요청한 트랜잭션 size")
    # print(np.average(rtx_size))
    # print(np.max(rtx_size))
    # print(np.min(rtx_size))

    # print("요청하지 않은 트랜잭션 fee")
    # print(np.average(utx_fee))
    # print(np.max(utx_fee))
    # print(np.min(utx_fee))

    # print("요청하지 않은 트랜잭션 size")
    # print(np.average(utx_size))
    # print(np.max(utx_size))
    # print(np.min(utx_size))