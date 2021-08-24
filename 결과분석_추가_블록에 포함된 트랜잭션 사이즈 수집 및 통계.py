## 특정 높이의 블록 트랜잭션 정보 수집

import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# 변수 선언
# 콜렉션
collection_tx = []

# 트랜잭션 목록
tx_list = []


# rpc 연결
def rpc_connect():
    rpc_connection = AuthServiceProxy("http://bitcoinrpc:660219@127.0.0.1:8332")
    return rpc_connection


# 몽고 db 연결
# def connect_mongoDB():
#     global collection_tx
#
#     # 서브 노드의 요청한 트랜잭션 locktime
#     myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
#     mydb = myclient['prefilledtxn']
#     collection_tx = mydb["BlockTxSize"]
#
#     return collection_tx

## 5월 5일 681905 - 682075
## 5월 6일 682076 - 682231


# 특정 높이의 블록 hash 값 얻기
def get_blockHash(rpc_connection):
    blockhash = []
    blockheight_start = 689310
    blockheight_end = 690673

    while(blockheight_start <= blockheight_end):
        blockhash.append([blockheight_start, rpc_connection.getblockhash(blockheight_start)])
        blockheight_start = blockheight_start + 1

    return blockhash


# 해당 블록이 보유하고 있는 트랜잭션 아이디를 모두 받아옴
def get_tx_list(rpc_connection):
    global tx_list

    blockhash = get_blockHash(rpc_connection)

    for block in blockhash: # block은 [height, hash]
        block_info = rpc_connection.getblock(block[1])
        tmp_tx_list = block_info["tx"]
        # 블록의 트랜잭션을 tx_list에 넣음
        for tx in tmp_tx_list:
            tx_list.append([block[1],tx]) # tx_list [blockHash, txHash]


# 트랜잭션의 정보를 찾고 그 중 트랜잭션 사이즈를 따로 모아 평균을 냄
def get_tx_info(rpc_connection):
    global tx_list
    tx_size = []
    count = 0
    for tx in tx_list:
        try:
            tx_info = rpc_connection.getrawtransaction(tx[1], True, tx[0]) # txhash, false=string/true=json, txblockhash
            tx_size.append(tx_info["size"])
            count = count + 1
            if count % 1000 == 0 :
                print("현재 저장된 개수는 " + str(count) + " 개 입니다.")
        except:
            continue

    print("모든 트랜잭션에 대한 정보를 모았습니다.")
    print("트랜잭션 평균 사이즈")
    print(np.average(tx_size))
    tpd = pd.Series(tx_size)
    print("트랜잭션 사이즈 Q3")
    print(tpd.quantile(.75))
    print("트랜잭션 사이즈 최대값")
    print(np.max(tx_size))


# # 몽고 db에 저장
# def save_mongo_db(collection, db_json):
#
#     collection.insert_one(db_json)
#

if __name__ == '__main__':
    rpc_connection = rpc_connect()
    get_tx_list(rpc_connection)
    get_tx_info(rpc_connection)
