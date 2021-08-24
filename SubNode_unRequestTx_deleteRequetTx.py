 ## 요청한 트랜잭션을 삭제해서 요청하지 않은 트랜잭션 목록 완성하기

import pymongo
from pymongo import MongoClient
import time
import datetime

# 변수 선언
# 콜렉션
collection_requestTx = []
collection_unRequestTx = []

# 요청한 아이디 트랜잭션 목록
tx_list = [] 

db_json = {}


# 몽고 db 연결
def connect_mongoDB():
    global collection_requestTx
    global collection_unRequestTx

    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    # 요청한 트랜잭션의 정보를 담은 블록
    collection_requestTx = mydb["SubNode_requestTx_locktime"]
    # 요청하지 않은 트랜잭션
    collection_unRequestTx = mydb["SubNode_unRequestTx"]


# 요청한 트랜잭션 id를 받아옴
def make_request_tx_list():
    global collection_requestTx
    global tx_list

    take_data = collection_requestTx.find({},{"_id":1})

    for tx in take_data:
        tx_list.append(tx["_id"])

# 요청한 트랜잭션을 삭제해서 요청하지 않은 트랜잭션 db를 완성시킴       
def del_requestTx():
    global collection_unRequestTx
    global tx_list

    for tx in tx_list:
        collection_unRequestTx.delete_one({"_id": tx})
    


if __name__ == '__main__':
    connect_mongoDB()
    make_request_tx_list()
    del_requestTx()
