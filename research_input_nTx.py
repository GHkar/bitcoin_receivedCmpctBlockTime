import pymongo
from pymongo import MongoClient
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging

# 몽고 db 연결
myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
mydb = myclient['bitcoin']
collection = mydb["SubNode_cmpctblock_nTx_654000-656000"]

db_json = {}

# rpc 연결
rpc_connection = AuthServiceProxy("http://bitcoinrpc:660219@127.0.0.1:8333")


blockhash = []
blockheight_start = 660000
blockheight_end = 661300

# 블록 hash 값 얻기
while(blockheight_start < blockheight_end):
    blockhash.append([blockheight_start, rpc_connection.getblockhash(blockheight_start)])
    blockheight_start = blockheight_start + 1

# 블록 ntx 값 얻기
i = 0
while(i < len(blockhash)): 
    height,hash = blockhash[i]
    block = rpc_connection.getblock(hash)
    db_json['_id'] = height
    db_json['hash'] = hash
    db_json['ntx'] = block['nTx']
    collection.insert_one(db_json)

    db_json = {}
    i = i+1



