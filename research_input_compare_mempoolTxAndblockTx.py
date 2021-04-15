import pymongo
from pymongo import MongoClient
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
from datetime import datetime

# 몽고 db 연결
myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")   # 미니PC 1
mydb = myclient['bitcoin']
collection = mydb["SubNode_cmpctblock_compareMempool"]

takeDataClient = pymongo.MongoClient("mongodb://210.125.31.237:80/")    # 미니PC 2
mydb2 = takeDataClient['bitcoin']
collection_mempool_tx_list = mydb2["SubNode_mempool_mempool_tx_list"]
collection_mempool_tx_info = mydb2["SubNode_mempool_tx_info"]

db_json = {}
take_txid = []
correct_txid = []
uncorrect_txid = []

# rpc 연결
rpc_connection = AuthServiceProxy("http://bitcoinrpc:660219@127.0.0.1:8333")

#============================================================ 해시, 높이, 날짜 입력 필수

blockhash = "000000000000000000033ddf18782536753594861a48822727359d7abf136106"
blockheight = 661246
totalTxSize = 0

mempool_date = datetime.strptime("2020-12-14 07:21:27.167", '%Y-%m-%d %H:%M:%S.%f')
take_data = collection_mempool_tx_list.find({"_id": mempool_date})

#============================================================

for data in take_data:
    take_txid = data["txid"]

# 비교
block = rpc_connection.getblock(blockhash)
txlist = block['tx']
for tx in txlist :
    if tx in take_txid:
        correct_txid.append(tx)

uncorrect_txid = list(set(txlist) - set(correct_txid))



db_json['_id'] = blockheight
db_json['hash'] = blockhash
db_json['correctTxCount'] = len(correct_txid)
db_json['uncorrectTxCount'] = len(uncorrect_txid)
db_json['nTx'] = block["nTx"]
db_json['unCorrectTxList'] = uncorrect_txid
collection.insert_one(db_json)

db_json = {}




