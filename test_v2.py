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
nodeNum = "node1"

# rpc 연결
def rpc_connect():
    rpc_connection = AuthServiceProxy("http://bitcoinrpc:660219@127.0.0.1:8333")
    return rpc_connection

# 몽고 db 연결
def connect_mongoDB():
    global collection_mempool_tx_info
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection_mempool_tx_info = mydb["mempool_tx_info_"+nodeNum]

# 멤풀 내 트랜잭션 정보 입력
def make_mempoolTxInfo_json(tx, mempoolTxInfo_json, now_mempoolTxInfo, time, txFirst):
    if txFirst :
        mempoolTxInfo_json["_id"] = tx
    mempoolTxInfo_json["checkTime"] = time
    mempoolTxInfo_json["txinfo"] = {}

  
 # 몽고 db 저장 
def save_mongo_db(collection, input_json):
    collection.insert_one(input_json)

# 몽고 db modify
def modify_mongo_db(tx, collection, input_json):
    collection.find_one_and_update({'_id': tx}, {"$set" : input_json})


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
# tx가 있으면 1
def checkTx(tx):
    if collection_mempool_tx_info.count_documents({'_id': tx})> 0:
        return 1
    else :
        return 0


# Tx 정보 얻기
def getTxList(rpc_connection, now_time):
    try :
        connect_mongoDB()
        mempoolTxInfo_json = {}

        # 현재 메모리 풀에 들어있는 트랜잭션 리스트를 받음
        now_mempoolTxList = {'a','b','c','d','e'}
        # 각 트랜잭션에 대한 정보 넣기
        for tx in now_mempoolTxList:
            try:
                now_mempoolTxinfo = {}
                check = checkTx(tx)
                if check == 0:  # 새로운 tx
                    make_mempoolTxInfo_json(tx, mempoolTxInfo_json, now_mempoolTxinfo, now_time, True)
                    save_mongo_db(collection_mempool_tx_info, mempoolTxInfo_json)
                elif check == 1: # 모두 존재
                    make_mempoolTxInfo_json(tx, mempoolTxInfo_json, now_mempoolTxinfo, now_time, False)
                    modify_mongo_db(tx, collection_mempool_tx_info, mempoolTxInfo_json)

                mempoolTxInfo_json = {}
            except Exception as ex:
                print("err : " + str(ex))

        now_mempoolTxList = {}
    
        print("save complete : " + str(now_time))

    except Exception as ex:
        print("err : " + str(ex))
    
#schedule.every().thursday.at("18:00").do(getTxListTimer())  # 매 목요일 6시마다 실행이라는 함수지만, 그냥 6시에 모두 동일하게 시작하기 위해 사용

if __name__ == '__main__':
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    rpc_connection = rpc_connect()
    getTxList(rpc_connection,now_time)
    # while True:
    #     # 스케쥴을 돌리기 위한 함수, 매 1초마다 갱신되어 스케쥴 할 거리를 찾음
    #     schedule.run_pending()
    #     time.sleep(1)
    #     if(datetime.datetime.now() > datetime.datetime.strptime("2021-4-15 18:00:00", "%Y-%m-%d %H:%M:%S")): # 특정시간이 지나면 while 문 나가기
    #         break   # 부하를 줄이기 위하여 while 문은 끔
