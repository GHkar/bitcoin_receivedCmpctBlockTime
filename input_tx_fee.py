# 트랜잭션 fee를 계산

import pymongo
from pymongo import MongoClient
import bson

# 몽고 db 연결
def connect_mongoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["SubNode_0420BlocksTx"]
    
    return collection

def connect_mongoDB2():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["SubNode_0420BlocksTx_fee"]
    
    return collection 

def calculate_fee(collection, collection2):
    take_data = collection.find({}) # 트랜잭션
    tx = {}
    for td in take_data:
        vin = td["vin"]
        vout = td["vout"]
        vin_total = 0.0
        vout_total = 0.0
        fee_cal = 0.0

        coinbase = False

        for i in vin:
            key_vin = i.keys()
            for ki in key_vin: # vin이 coin base 인 경우에는 fee가 0
                if ki == "coinbase":
                    coinbase  = True
                    break
                elif ki == "txid" :
                    coinbase = False
                    break
            

            if coinbase :
                fee_cal = 0

            else :
                # count_documents({"_id":i["txid"]})
                if 0 < collection.find({"_id":i["txid"]}).count() : # vin에서 이전 tx를 찾음
                    before_tx = collection.find_one({"_id":i["txid"]})
                    before_vout = before_tx["vout"]
                    for bv in before_vout: # vout에서 vin에 맞는 index 찾기
                        if bv["n"] == i["vout"]:
                            vin_total = vin_total + float(str(bv["value"]))
                            break
                    for o in vout:
                        vout_total = vout_total + float(str(o["value"]))

                fee_cal = vin_total - vout_total


        tx["_id"] = td["_id"]
        tx["blockHeight"] = td["blockHeight"]
        tx["blockHash"] = td["blockhash"]
        tx["size"] = td["size"]
        tx["fee"] = fee_cal
        
        if tx["fee"] > 0 :
            collection2.insert_one(tx)
        coinbase = False

if __name__ == '__main__':
    calculate_fee(connect_mongoDB(),connect_mongoDB2())
