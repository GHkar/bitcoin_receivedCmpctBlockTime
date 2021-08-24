import pymongo
from pymongo import MongoClient
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging

# 몽▒|  db ▒~W▒결
myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
mydb = myclient['prefilledtxn']
collection = mydb["nTx"]

db_json = {}

# rpc ▒~W▒결
rpc_connection = AuthServiceProxy("http://bitcoinrpc:660219@127.0.0.1:8333")


blockhash = []
blockheight_start = 686782
blockheight_end = 686909

# ▒~T▒~] hash ▒~R ▒~V▒기
while(blockheight_start < blockheight_end):
    blockhash.append([blockheight_start, rpc_connection.getblockhash(blockheight_start)])
    blockheight_start = blockheight_start + 1

# ▒~T▒~] ntx ▒~R ▒~V▒기
i = 0
while(i < len(blockhash)):
    height,hash = blockhash[i]
    block = rpc_connection.getblock(hash)
    db_json['_id'] = height
    db_json['ntx'] = block['nTx']
    collection.insert_one(db_json)

    db_json = {}
    i = i+1

