## 트랜잭션 별로 6개의노드에서 메모리 풀에 들어온 시간을 수집

import pymongo
from pymongo import MongoClient
import time
import datetime

# 변수 선언
# 콜렉션
nodes = []
collection_requestTx_Block = []
collection_tx_times = []

# 요청한 아이디 트랜잭션 목록
tx_list = [] 

db_json = {}

# 몽고 db 연결
def connect_mongoDB():
    global nodes
    global collection_requestTx_Block
    global collection_tx_times

    # 요청한 트랜잭션의 정보를 담은 블록
    myclient = pymongo.MongoClient("mongodb://210.125.31.245:1000/")
    mydb = myclient['Test']
    collection_requestTx_Block = mydb["Block"]
    
    # 노드 1 ~ 6 + 트랜잭션 생성 시간을 담을 콜렉션
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    nodes.append(mydb["mempool_tx_info_node1"])
    nodes.append(mydb["mempool_tx_info_node2"])
    collection_tx_times = mydb["6Nodes_tx_memPoolInTime"]

    myclient = pymongo.MongoClient("mongodb://210.125.29.228:80/")
    mydb = myclient['bitcoin']
    nodes.append(mydb["mempool_tx_info_node3"])
    nodes.append(mydb["mempool_tx_info_node4"])

    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['bitcoin']
    nodes.append(mydb["mempool_tx_info_node5"])
    nodes.append(mydb["mempool_tx_info_node6"])

# 요청한 트랜잭션 리스트를 만듦
def make_request_tx_list():
    global collection_requestTx_Block
    global tx_list
     # 트랜잭션을 요청한 블록을 불러 옴
    take_data = collection_requestTx_Block.find({"height":{"$gte":679792,"$lte":679913}})
    
    # 모든 트랜잭션의 해시를 찾음
    for find_height in take_data:
        for tx_index in find_height["tx"]:
            tx_list.append(find_height["tx"][tx_index]['txid'])
    
# 노드들에서 해당 트랜잭션에 대한 정보가 있는지 찾음
def find_tx_in_Nodes():
    global nodes
    global collection_tx_times
    global db_json
 
    for tx_id in tx_list:
        try:
            times = []
            nodeNum = 1
            for node in nodes:
                if node.count_documents({'_id': tx_id})> 0: # 해당 노드에 트랜잭션이 있다면
                    tx = node.find_one({'_id': tx_id})
                    times.append([nodeNum, tx["txinfo"]["time"]]) # times에 추가
                nodeNum = nodeNum+1
            make_db_json(tx_id, times)
            save_mongo_db(collection_tx_times)
            db_json = {}            
        except :
            continue

# 몽고 db에 저장
def save_mongo_db(collection):
    global db_json

    collection.insert_one(db_json)

def make_db_json(tx_id, times):
    global db_json

    db_json["_id"] = tx_id
    db_json["times"] = times


if __name__ == '__main__':
    connect_mongoDB()
    make_request_tx_list()
    find_tx_in_Nodes()





    # times = collection_tx_times.find({},{"times":1})
    # for time in times:
    #     length = len(time["times"])
    #     listT = time["times"]
    #     for tt in listT:
    #         print(tt[0])