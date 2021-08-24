 ## 요청한 트랜잭션을 삭제해서 요청하지 않은 트랜잭션 목록 완성하기

import pymongo
from pymongo import MongoClient
import time
import datetime

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

    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection_1 = mydb["50-1Blocksize"]
    collection_2 = mydb["50-2Blocksize"]
    collection_3 = mydb["50-3Blocksize"]
    collection_4 = mydb["50-4Blocksize"]
    collection_5 = mydb["pb30-Blocksize"]
    collection_6 = mydb["pb40-Blocksize"]
    collection_7 = mydb["pbm-Blocksize"]


def del_requestTx():
    global collection_1
    global collection_2
    global collection_3
    global collection_4
    global collection_5
    global collection_6
    global collection_7

    collection_1.delete_many({"_id": {"$lt": 695240 }})#, "$lt":688987} })
    collection_2.delete_many({"_id": {"$lt": 695240 }})#, "$lt":688987} })
    collection_3.delete_many({"_id": {"$lt": 695240 }})#, "$lt":688987} })
    collection_4.delete_many({"_id": {"$lt": 695240 }})#, "$lt":688987} })
    collection_5.delete_many({"_id": {"$lt": 695240 }})#, "$lt":688987} })
    collection_6.delete_many({"_id": {"$lt": 695240 }})#, "$lt":688987} })
    collection_7.delete_many({"_id": {"$lt": 695240 }})#, "$lt":688987} })
    # {"$gt":682075} {"$lt":681905}

if __name__ == '__main__':
    connect_mongoDB()
    del_requestTx()
