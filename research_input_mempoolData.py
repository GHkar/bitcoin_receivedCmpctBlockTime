from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime
import simplejson as json
from bson.decimal128 import Decimal128

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
    myclient = pymongo.MongoClient("mongodb://210.125.31.237:80/")
    mydb = myclient['bitcoin']
    collection_mempool_info = mydb["SubNode_mempool_info"]
    collection_mempool_tx_list = mydb["SubNode_mempool_mempool_tx_list"]
    collection_mempool_tx_info = mydb["SubNode_mempool_tx_info"]



def make_mempoolInfo_json(mempoolInfo_json, now_mempoolInfo, time):
    mempoolInfo_json['_id'] = time
    mempoolInfo_json['currentTx'] = now_mempoolInfo['size']
    mempoolInfo_json['currentSize'] = now_mempoolInfo['bytes']
    mempoolInfo_json['maxMempoolSize'] = now_mempoolInfo['maxmempool']

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

def getMempoolData(rpc_connection):
    mempoolInfo_json = {}
    mempoolTxList_json = {}
    mempoolTxInfo_json = {}

    now_time = datetime.now()

    now_mempoolInfo = rpc_connection.getmempoolinfo()
    now_mempoolTxList = rpc_connection.getrawmempool()
    
    
    make_mempoolInfo_json(mempoolInfo_json, now_mempoolInfo, now_time)
    make_mempoolTxList_json(mempoolTxList_json, now_mempoolTxList, now_time)

    save_mongo_db(collection_mempool_info, mempoolInfo_json)
    save_mongo_db(collection_mempool_tx_list, mempoolTxList_json)

    for tx in mempoolTxList_json['txid']:
        try:
            now_mempoolTxinfo = rpc_connection.getmempoolentry(tx)
            make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time)
            save_mongo_db(collection_mempool_tx_info, mempoolTxInfo_json)
            mempoolTxInfo_json = {}
        except :
            continue

    mempoolInfo_json = {}
    mempoolTxList_json = {}
    return now_time

    



while True:
    try :
        connect_mongoDB()
        now_time = getMempoolData(rpc_connect())
        print("save " + str(now_time))
        time.sleep(10)

    except Exception as ex:
        print("err : " + str(ex))
        continue
