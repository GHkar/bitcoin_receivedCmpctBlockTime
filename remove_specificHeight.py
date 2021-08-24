 ## 요청한 트랜잭션을 삭제해서 요청하지 않은 트랜잭션 목록 완성하기

import pymongo
from pymongo import MongoClient
import time
import datetime

collection_1 = []
collection_2 = []
collection_3 = []
collection_4 = []

# 몽고 db 연결
def connect_mongoDB():
    global collection_1
    global collection_2
    global collection_3
    global collection_4

    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["1requestTxn"]
    collection_2 = mydb["2requestTxn"]
    collection_3 = mydb["3requestTxn"]
    collection_4 = mydb["4requestTxn"]


def del_requestTx():
    global collection_1
    global collection_2
    global collection_3
    global collection_4

    collection_1.delete_many({"_id": {"$gt":688650 , "$lt":688987} })
    collection_2.delete_many({"_id": {"$gt":688650 , "$lt":688987} })
    collection_3.delete_many({"_id": {"$gt":688650 , "$lt":688987} })
    collection_4.delete_many({"_id": {"$gt":688650 , "$lt":688987} })
    # {"$gt":682075} {"$lt":681905}

if __name__ == '__main__':
    connect_mongoDB()
    del_requestTx()
