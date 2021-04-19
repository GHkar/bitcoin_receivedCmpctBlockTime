from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pymongo
from pymongo import MongoClient
import time
import datetime
import simplejson as json
from bson.decimal128 import Decimal128
import threading
import schedule

# 변수 선언
collection_mempool_tx_info = []
nodeNum = 2

# rpc 연결
def rpc_connect():
    rpc_connection = AuthServiceProxy("http://bitcoinrpc:660219@127.0.0.1:8333")
    return rpc_connection

# 몽고 db 연결
def connect_mongoDB():
    global collection_mempool_tx_info
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection_mempool_tx_info = mydb["mempool_tx_info"]

# 멤풀 내 트랜잭션 정보 입력
def make_mempoolTxInfo_json(tx, mempoolTxInfo_json, now_mempoolTxInfo, time, txStart):
    if txStart :
        mempoolTxInfo_json["_id"] = tx    
        mempoolTxInfo_json["nodeNum"] = { str(nodeNum) : {}}
        mempoolTxInfo_json["nodeNum"][str(nodeNum)] = {"checkTime":time, "txinfo":{}}
    else : 
        mempoolTxInfo_json[str(nodeNum)] = {"checkTime":time, "txinfo":{}}
    

    
    # 구조
    # {
    #     "_id" : tx,
    #     "nodeNum" : {
    #         "1" : {
    #             "checkTime" : time,
    #             "txinfo" : {
    #                 "vsize" : now_mempoolTxInfo['vsize'],
    #                 "fees" : {
    #                     "base" : now_mempoolTxInfo['fees']['base']
    #                 }
    #             }
    #         }
    #     }
    # }
    
  
 # 몽고 db 저장 
def save_mongo_db(collection, input_json):
    collection.insert(input_json)

# 몽고 db modify
def modify_mongo_db(collection, tx, input_json):
    collection.find_and_modify({'_id': tx, 'nodeNum.'+str(nodeNum): {"$exists":True}}, input_json)

# 몽고 db push
def push_mongo_db(collection, tx, input_json):
    collection_mempool_tx_info.find_one_and_update({'_id': tx, 'nodeNum.'+str(nodeNum): {"$exists":False}}, {"$set": {'nodeNum.'+str(nodeNum) : {} }})

    
# 이미 존재하는 트랜잭션인지 체크
# tx가 없는 경우 0
# tx가 있고, 내 노드에 대한 것도 있는 경우 1
# tx가 있는데, 내 노드에 대한 것은 없는 경우 2
def checkTx(tx):
    connect_mongoDB()
    if collection_mempool_tx_info.find({'_id': tx}).count() > 0:
        if collection_mempool_tx_info.find({'_id' : 'a', "nodeNum." + str(nodeNum) : {"$exists":True}}).count() > 0:
            return 1
        else :
            return 2
    else :
        return 0


# Tx 정보 얻기
def getTxList(rpc_connection, now_time):
    try :
        connect_mongoDB()
        mempoolTxInfo_json = {}

        # 현재 메모리 풀에 들어있는 트랜잭션 리스트를 받음
        now_mempoolTxList = {'a'}
        # 각 트랜잭션에 대한 정보 넣기
        for tx in now_mempoolTxList:
            try:
                now_mempoolTxinfo = {}
                check = checkTx(tx)
                if check == 0:  # 새로운 tx
                    make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time, True)
                    save_mongo_db(collection_mempool_tx_info, mempoolTxInfo_json)
                elif check == 1: # 모두 존재
                    make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time, True)
                    modify_mongo_db(collection_mempool_tx_info, tx, mempoolTxInfo_json)
                elif check == 2 : # tx는 있으나, 내 것은 없음
                    make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time, False)
                    push_mongo_db(collection_mempool_tx_info, tx, mempoolTxInfo_json)

                mempoolTxInfo_json = {}
            except Exception as ex:
                print("err : " + str(ex))

        now_mempoolTxList = {}
    

    except Exception as ex:
        print("err : " + str(ex))
    

if __name__ == '__main__':
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    rpc_connection = rpc_connect()
    getTxList(rpc_connection, now_time)
