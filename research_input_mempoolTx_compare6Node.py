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
nodeNum = 1

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
    mempoolTxInfo_json["nodeNum"][str(nodeNum)]["txinfo"] = {
        "vsize": now_mempoolTxInfo['vsize'],
        "weight" : now_mempoolTxInfo['weight'],
        "fee" : Decimal128(now_mempoolTxInfo['fee']),
        "modifiedfee" : Decimal128(now_mempoolTxInfo['modifiedfee']),
        "time" : datetime.datetime.utcfromtimestamp(now_mempoolTxInfo['time']) + datetime.timedelta(hours=9), # epoch sec을 dateTime으로 변경 후, 한국 시간으로 변경하기
        "height" : now_mempoolTxInfo['height'],
        "descendantcount" : now_mempoolTxInfo['descendantcount'],
        "descendantsize": now_mempoolTxInfo['descendantsize'],
        "descendantfees": now_mempoolTxInfo['descendantfees'],
        "ancestorcount": now_mempoolTxInfo['ancestorcount'],
        "ancestorsize": now_mempoolTxInfo['ancestorsize'],
        "ancestorfees": now_mempoolTxInfo['ancestorfees'],
        "wtxid": now_mempoolTxInfo['wtxid'],
        "depends": now_mempoolTxInfo['depends'],
        "spentby": now_mempoolTxInfo['spentby'],
        "bip125-replaceable": now_mempoolTxInfo['bip125-replaceable'],
        "unbroadcast": now_mempoolTxInfo['unbroadcast'],
        "fees":{}
    }
    mempoolTxInfo_json["nodeNum"][str(nodeNum)]["txinfo"]["fees"] = {
        "base" : Decimal128(now_mempoolTxInfo['fees']['base']),
        "modified" : Decimal128(now_mempoolTxInfo['fees']['modified']),
        "ancestor" : Decimal128(now_mempoolTxInfo['fees']['ancestor']),
        "descendant" : Decimal128(now_mempoolTxInfo['fees']['descendant'])
    }
    
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

# 몽고 db update
def update_mongo_db(collection, tx, input_json):
    collection.updete({'_id': tx}, {'nodeNum': str(nodeNum)}, input_json)

# 몽고 db push
def push_mongo_db(collection, tx, input_json):
    collection.update({'_id': tx}, { "$push" : input_json})


# 시간마다 threading (1분)s
def getTxListTimer():
    threading.Timer(60, getTxListTimer).start()
    
    # 멤풀 정보 id로 사용할 현재 시간을 년, 월, 날, 시, 분으로 표현
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print("save start : " + now_time)
    rpc_connection = rpc_connect()
    getTxList(rpc_connection,now_time)
   
    
# 이미 존재하는 트랜잭션인지 체크
# tx가 없는 경우 0
# tx가 있고, 내 노드에 대한 것도 있는 경우 1
# tx가 있는데, 내 노드에 대한 것은 없는 경우 2
def checkTx(tx):
    if collection_mempool_tx_info.find({'_id': tx}):
        if collection_mempool_tx_info.find({'nodeNum':str(nodeNum)}):
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
        now_mempoolTxList = rpc_connection.getrawmempool()
        # 각 트랜잭션에 대한 정보 넣기
        for tx in now_mempoolTxList:
            try:
                now_mempoolTxinfo = rpc_connection.getmempoolentry(tx)
                check = checkTx(tx)
                if check == 0:  # 새로운 tx=
                    make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time, True)
                    save_mongo_db(collection_mempool_tx_info, mempoolTxInfo_json)
                elif check == 1: # 모두 존재
                    make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time, True)
                    update_mongo_db(collection_mempool_tx_info, tx, mempoolTxInfo_json)
                elif check == 2: # tx는 있으나, 내 것은 없음
                    make_mempoolTxInfo_json(tx,mempoolTxInfo_json, now_mempoolTxinfo, now_time, False)
                    push_mongo_db(collection_mempool_tx_info, tx, mempoolTxInfo_json)

                mempoolTxInfo_json = {}
            except Exception as ex:
                print("err : " + str(ex))

        now_mempoolTxList = {}
    
        print("save complete : " + str(now_time))

    except Exception as ex:
        print("err : " + str(ex))
    
#schedule.every().thursday.at("18:00").do(getTxListTimer())  # 매 목요일 6시마다 실행이라는 함수지만, 그냥 6시에 모두 동일하게 시작하기 위해 사용

if __name__ == '__main__':
    getTxListTimer()

    # while True:
    #     # 스케쥴을 돌리기 위한 함수, 매 1초마다 갱신되어 스케쥴 할 거리를 찾음
    #     schedule.run_pending()
    #     time.sleep(1)
    #     if(datetime.datetime.now() > datetime.datetime.strptime("2021-4-15 18:00:00", "%Y-%m-%d %H:%M:%S")): # 특정시간이 지나면 while 문 나가기
    #         break   # 부하를 줄이기 위하여 while 문은 끔
