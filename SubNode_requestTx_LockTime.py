## 요청한 트랜잭션의 locktime 구하기

import pymongo
from pymongo import MongoClient
import time
import datetime

# 변수 선언
# 콜렉션
collection_requestTx_Block = []
collection_requestTx_lockTime = []

# 요청한 아이디 트랜잭션 목록
tx_list = [] 

db_json = {}


# 몽고 db 연결
def connect_mongoDB():
    global collection_requestTx_Block
    global collection_requestTx_lockTime

    # 요청한 트랜잭션의 정보를 담은 블록
    myclient = pymongo.MongoClient("mongodb://210.125.31.245:1000/")
    mydb = myclient['Test']
    collection_requestTx_Block = mydb["Block"]
    
    # 서브 노드의 요청한 트랜잭션 locktime
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection_requestTx_lockTime = mydb["SubNode_requestTx_locktime"]


# 요청한 트랜잭션 리스트를 만듦
def make_request_tx_list():
    global collection_requestTx_Block
    global tx_list
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_requestTx_Block.find({"height":{"$gte":679792,"$lte":679913}})
    
    # 모든 트랜잭션의 정보를 찾음
    for find_height in take_data:
        for tx_index in find_height["tx"]:
            tx_list.append(find_height["tx"][tx_index])

def get_loctTime_size():
    global collection_requestTx_lockTime
    for tx in tx_list:
        make_db_json(tx["txid"], tx["locktime"], tx["size"])
        save_mongo_db(collection_requestTx_lockTime)


# 몽고 db에 저장
def save_mongo_db(collection):
    global db_json

    collection.insert_one(db_json)

def make_db_json(tx_id, lockTime, size):
    global db_json

    db_json["_id"] = tx_id
    db_json["lockTime"] = lockTime
    db_json["size"] = size


if __name__ == '__main__':
    connect_mongoDB()
    make_request_tx_list()
    get_loctTime_size()
