# 트랜잭션별로 트랜잭션 생성 시각 유추

import pymongo
from pymongo import MongoClient
import time
import datetime
from datetime import timedelta

# 변수 선언
# 콜렉션
collection_tx_generationTime = []
collection_tx_times = []

# 요청한 아이디 트랜잭션 목록

db_json = {}

# 몽고 db 연결
def connect_mongoDB():
    global collection_tx_generationTime
    global collection_tx_times

    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']

    collection_tx_generationTime = mydb["6Nodes_tx_generationTime"]
    collection_tx_times = mydb["6Nodes_tx_memPoolInTime"]

# 요청한 트랜잭션 데이터를 가져와서 시각 평균 구하기
def calculate_tx_generattionTime():
    global collection_tx_times
    global collection_tx_generationTime
    length = 0

     # 트랜잭션 타임 데이터 불러오기
    txWithTime = collection_tx_times.find({},{"times":1})
    for tx in txWithTime:
        try :
            length = len(tx["times"])
            if length != 0:
                times = tx["times"]
                meanTime = calculate_dateTime_mean(times,length)
                make_db_json(tx["_id"], meanTime)
                save_mongo_db(collection_tx_generationTime)
        except :
            continue

# dateTime의 평균 구하기        
def calculate_dateTime_mean(times,length):
    sumTime = 0
    for t in times:
        sumTime += t[1].timestamp() # 초로 바꿈

    return datetime.datetime.fromtimestamp(sumTime/length) #초를 다시 dateTime으로


# 몽고 db에 저장
def save_mongo_db(collection):
    global db_json

    collection.insert_one(db_json)

def make_db_json(tx_id, time):
    global db_json

    db_json["_id"] = tx_id
    db_json["times"] = time


if __name__ == '__main__':
    connect_mongoDB()
    calculate_tx_generattionTime()



    # times = collection_tx_times.find({},{"times":1})
    # for time in times:
    #     length = len(time["times"])
    #     listT = time["times"]
    #     for tt in listT:
    #         print(tt[0])