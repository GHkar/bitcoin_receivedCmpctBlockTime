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
    collection = mydb["log_MainNode_inv_JaccardIndex_includePartSet"]
    
    return collection 

def calculate_JaccardIndex(collection, collection2):
    start_height = 681905
    end_hegiht = 682075
    while start_height <= end_hegiht:
        take_data = collection.find({"height":start_height})
        set_inv = []
        part_inv = []
        block = {}
        count_inv = {}
        frequency = 0
        for td in take_data:
            set_inv.append(set(td["invTx"]))
            part_inv.extend(td["invTx"])

        # 모든 트랜잭션을 합쳐서 빈도 수 구함. 빈도가 1이상, 즉 중복되는 것이 있는 트랜잭션의 경우 frequency를 1 더함
        for pi in part_inv:
            count_inv[pi] = count_inv.get(pi, 0) + 1
        for key, value in count_inv.items():
            if value > 1 :
                frequency = frequency + 1
        
        length = len(set_inv)
        if length == 4 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 5 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 6 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 7 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 8 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 9 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 10 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 11 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 12 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10], set_inv[11])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
        elif length == 13 :
            union_inv = set.union(set_inv[0],set_inv[1],set_inv[2],set_inv[3],set_inv[4],set_inv[5],set_inv[6],set_inv[7],set_inv[8],set_inv[9], set_inv[10], set_inv[11], set_inv[12])
            jaccard = frequency/len(union_inv)
            block["_id"] = start_height
            block["inv_jaccard"] = jaccard
            collection2.insert_one(block)
    
        start_height = start_height+1
           

if __name__ == '__main__':
    calculate_JaccardIndex(connect_mongoDB(),connect_mongoDB2())
