 ## inv 메시지 트랜잭션 유사도 분석

import pymongo
from pymongo import MongoClient
import time
import datetime

# 몽고 db 연결
def connect_mongoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["log_MainNode_received_Inv"]
    
    return collection

def connect_mongoDB2():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["log_MainNode_inv_JaccardIndex"]
    
    return collection 

def calculate_JaccardIndex(collection, collection2):
    start_height = 681905
    end_hegiht = 682075
    while start_height <= end_hegiht:
        take_data = collection.find({"height":start_height})
        set_inv = []
        block = {}
        for td in take_data:
            set_inv.append(set(td["invTx"]))
        length = len(set_inv)
        if length == 4 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 5 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 6 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[4],set_inv[5])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 7 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 8 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 9 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 10 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 11 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 12 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10], set_inv[11])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10], set_inv[11])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 13 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10], set_inv[11], set_inv[12])
            intersection_inv = set.intersection(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10], set_inv[11], set_inv[12])
            jaccard = len(intersection_inv)/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
    
        start_height = start_height+1
           

if __name__ == '__main__':
    calculate_JaccardIndex(connect_mongoDB(),connect_mongoDB2())
