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
collection_5 = []
collection_6 = []
collection_7 = []


# 몽고 db 연결
def connect_mongoDB():
    global collection_1
    global collection_2
    global collection_3
    global collection_4
    global collection_5
    global collection_6
    global collection_7

    # inv 데이터 가져오기
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["50-1receivedCmpctTime"]
    collection_2 = mydb["50-2receivedCmpctTime"]
    collection_3 = mydb["50-3receivedCmpctTime"]
    collection_4 = mydb["50-4receivedCmpctTime"]
    collection_5 = mydb["pb30-receivedCmpctTime"]
    collection_6 = mydb["pb40-receivedCmpctTime"]
    collection_7 = mydb["pbm-receivedCmpctTime"]



# 통계 내기
def calculate_size_fee_statistic():
    global collection_1
    global collection_2
    global collection_3
    global collection_4
    global collection_5
    global collection_6
    global collection_7

    # {"$gt":682075} {"$lt":681905}
    take_data1 = collection_1.find({})
    take_data2 = collection_2.find({})
    take_data3 = collection_3.find({})
    take_data4 = collection_4.find({})
    take_data5 = collection_5.find({})
    take_data6 = collection_6.find({})
    take_data7 = collection_7.find({})

    # 전달시간
    rt1 = []
    rt2 = []
    rt3 = []
    rt4 = []
    rt5 = []
    rt6 = []
    rt7 = []


    # 모든 트랜잭션의 정보를 찾음
    for td in take_data1:
            rt1.append(td["receiveTime_result"])

    for td in take_data2:
            rt2.append(td["receiveTime_result"])

    for td in take_data3:
            rt3.append(td["receiveTime_result"])

    for td in take_data4:
            rt4.append(td["receiveTime_result"])

    for td in take_data5:
            rt5.append(td["receiveTime_result"])

    for td in take_data6:
            rt6.append(td["receiveTime_result"])

    for td in take_data7:
            rt7.append(td["receiveTime_result"])


    print("전달시간1 평균")
    print(np.average(rt1))
    print("전달시간2 평균")
    print(np.average(rt2))
    print("전달시간3 평균")
    print(np.average(rt3))
    print("전달시간4 평균")
    print(np.average(rt4))
    print("전달시간5 평균")
    print(np.average(rt5))
    print("전달시간6 평균")
    print(np.average(rt6))
    print("전달시간7 평균")
    print(np.average(rt7))

    print("전달시간1 중앙값")
    print(np.median(rt1))
    print("전달시간2 중앙값")
    print(np.median(rt2))
    print("전달시간3 중앙값")
    print(np.median(rt3))
    print("전달시간4 중앙값")
    print(np.median(rt4))
    print("전달시간5 중앙값")
    print(np.median(rt5))
    print("전달시간6 중앙값")
    print(np.median(rt6))
    print("전달시간7 중앙값")
    print(np.median(rt7))

    print("전달시간1 표준편차")
    print(np.std(rt1))
    print("전달시간2 표준편차")
    print(np.std(rt2))
    print("전달시간3 표준편차")
    print(np.std(rt3))
    print("전달시간4 표준편차")
    print(np.std(rt4))
    print("전달시간5 표준편차")
    print(np.std(rt5))
    print("전달시간6 표준편차")
    print(np.std(rt6))
    print("전달시간7 표준편차")
    print(np.std(rt7))

    rt1p = pd.Series(rt1)
    rt2p = pd.Series(rt2)
    rt3p = pd.Series(rt3)
    rt4p = pd.Series(rt4)
    rt5p = pd.Series(rt5)
    rt6p = pd.Series(rt6)
    rt7p = pd.Series(rt7)

    print("전달시간1 IQR")
    q1 = rt1p.quantile(.25)
    q2 = rt1p.quantile(.5)
    q3 = rt1p.quantile(.75)
    print(q1)
    print(q2)
    print(q3)

    print("전달시간2 IQR")
    q1 = rt2p.quantile(.25)
    q2 = rt2p.quantile(.5)
    q3 = rt2p.quantile(.75)
    print(q1)
    print(q2)
    print(q3)

    print("전달시간3 IQR")
    q1 = rt3p.quantile(.25)
    q2 = rt3p.quantile(.5)
    q3 = rt3p.quantile(.75)
    print(q1)
    print(q2)
    print(q3)

    print("전달시간4 IQR")
    q1 = rt4p.quantile(.25)
    q2 = rt4p.quantile(.5)
    q3 = rt4p.quantile(.75)
    print(q1)
    print(q2)
    print(q3)

    print("전달시간5 IQR")
    q1 = rt5p.quantile(.25)
    q2 = rt5p.quantile(.5)
    q3 = rt5p.quantile(.75)
    print(q1)
    print(q2)
    print(q3)

    print("전달시간6 IQR")
    q1 = rt6p.quantile(.25)
    q2 = rt6p.quantile(.5)
    q3 = rt6p.quantile(.75)
    print(q1)
    print(q2)
    print(q3)

    print("전달시간7 IQR")
    q1 = rt7p.quantile(.25)
    q2 = rt7p.quantile(.5)
    q3 = rt7p.quantile(.75)
    print(q1)
    print(q2)
    print(q3)

    dictdata1 = {"rt1":rt1}
    dictdata2 = {"rt2":rt2}
    dictdata3 = {"rt3":rt3}
    dictdata4 = {"rt4":rt4}
    dictdata5 = {"rt5":rt5}
    dictdata6 = {"rt6":rt6}
    dictdata7 = {"rt7":rt7}

    df1 = df(dictdata1)
    df2 = df(dictdata2)
    df3 = df(dictdata3)
    df4 = df(dictdata4)
    df5 = df(dictdata5)
    df6 = df(dictdata6)
    df7 = df(dictdata7)

    fig, ax = plt.subplots()
#     plt.boxplot([df1["rt1"], df2["rt2"], df3["rt3"], df4["rt4"]], sym="b*")
#     #plt.boxplot([df2["rtx_size"], df4["utx_size"]])
#     plt.title("Block Received Time")
#     plt.xticks([1,2,3,4],['Origin','Size', 'Fee', 'Mempool in Time'])
#     plt.show()

    plt.boxplot([df1["rt1"], df2["rt2"], df3["rt3"], df4["rt4"]], sym="b*")
    #plt.boxplot([df2["rtx_size"], df4["utx_size"]])
    plt.title("Block Received Time")
    plt.xticks([1,2,3,4],['Origin','Size', 'Fee', 'Mempool in Time'])
    plt.show()




if __name__ == '__main__':
    connect_mongoDB()
    calculate_size_fee_statistic()
