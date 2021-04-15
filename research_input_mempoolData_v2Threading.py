from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime
import simplejson as json
from bson.decimal128 import Decimal128
import threading

# 변수 선언
collection_mempool_info = []
collection_mempool_tx_list = []
collection_mempool_tx_info = []

# rpc 연결
def rpc_connect():
    rpc_connection = AuthServiceProxy("http://bitcoinrpc:660219@127.0.0.1:8333")
    return rpc_connection

# 몽고 db 연결
def connect_mongoDB():
    global collection_mempool_info
    global collection_mempool_tx_list
    global collection_mempool_tx_info
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection_mempool_tx_list = mydb["SubNode_mempool_mempool_tx_list"]
    collection_mempool_tx_info = mydb["SubNode_mempool_tx_info"]


def make_mempoolTxList_json(mempoolTxList_json, now_mempoolTxList, time):
    mempoolTxList_json['_id'] = time
    mempoolTxList_json['txid'] = now_mempoolTxList

def make_mempoolTxInfo_json(tx, mempoolTxInfo_json, now_mempoolTxInfo, time):
    mempoolTxInfo_json['_id'] = tx
    mempoolTxInfo_json['time'] = time
    mempoolTxInfo_json['txinfo'] = now_mempoolTxInfo
    mempoolTxInfo_json['txinfo']['fees']['base'] = Decimal128(mempoolTxInfo_json['txinfo']['fees']['base'])
    mempoolTxInfo_json['txinfo']['fees']['modified'] = Decimal128(mempoolTxInfo_json['txinfo']['fees']['modified'])
    mempoolTxInfo_json['txinfo']['fees']['ancestor'] = Decimal128(mempoolTxInfo_json['txinfo']['fees']['ancestor'])
    mempoolTxInfo_json['txinfo']['fees']['descendant'] = Decimal128(mempoolTxInfo_json['txinfo']['fees']['descendant'])
    mempoolTxInfo_json['txinfo']['fee'] = Decimal128(mempoolTxInfo_json['txinfo']['fee'])
    mempoolTxInfo_json['txinfo']['modifiedfee'] = Decimal128(mempoolTxInfo_json['txinfo']['modifiedfee'])
  
def save_mongo_db(collection, json):
    collection.insert_one(json)


def getTxListTimer():
    threading.Timer(60, getTxListTimer).start()
    
    now_time = datetime.now()
    print("save start : " + str(now_time))
    rpc_connection = rpc_connect()
    getTxList(rpc_connection,now_time)
   
    

def getTxList(rpc_connection, now_time):
    try :
        connect_mongoDB()
        mempoolTxList_json = {}
        mempoolTxInfo_json = {}

        now_mempoolTxList = rpc_connection.getrawmempool()
        make_mempoolTxList_json(mempoolTxList_json, now_mempoolTxList, now_time)
        save_mongo_db(collection_mempool_tx_list, mempoolTxList_json)

        
    
        for tx in mempoolTxList_json['txid']:
            try:
                now_mempoolTxinfo = rpc_connection.getmempoolentry(tx)
                make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time)
                save_mongo_db(collection_mempool_tx_info, mempoolTxInfo_json)
                mempoolTxInfo_json = {}
            except :
                continue

        mempoolTxList_json = {}
    
        print("save complete : " + str(now_time))

    except Exception as ex:
        print("err : " + str(ex))
    


if __name__ == '__main__':
    getTxListTimer()
