# inv 패킷 내의 트랜잭션과 block 내에 포함된 트랜잭션의 유사도를 분석

import pymongo
from pymongo import MongoClient
import time
import datetime

# 몽고 db 연결
def connect_mongoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["log_SubNode_received_Inv"]
    
    return collection

def connect_mongoDB2():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["log_SubNode_inv_block_Tx_jaccardIndex"]
    
    return collection 

def calculate_JaccardIndex(collection, collection2):
    take_data = collection.find({}) # peer 들이 전달한 inv 메시지가 모여있음
    inv_tx = {}
    block = {}
    for td in take_data:
        inv_list = td["inv_list"]
        # 전달 받은 inv 내 모든 트랜잭션을 하나의 집합으로 만듦
        for inv in inv_list:
            inv_tx = set.union(set(inv["tx_list"]))

    intersection_inv = set.intersection()
    jaccard = len(intersection_inv)/len(union_inv)
    block["_id"] = start_height
    block["inv_block_tx_jaccard"] = jaccard
    collection2.insert_one(block)
           

if __name__ == '__main__':
    calculate_JaccardIndex(connect_mongoDB(),connect_mongoDB2())
