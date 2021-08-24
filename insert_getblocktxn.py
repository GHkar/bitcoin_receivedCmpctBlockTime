import pymongo
import json
import os
import glob
from pprint import pprint

path = "/home/dy/pcap_files"

def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['bitcoin']
    collection = mydb["SubNode_cmpctblock_received_time_per_height"]
    
    return collection

collection = connect_monogoDB()

file_dic = []
file_list = glob.glob(path+"/*")
for filename in file_list:
    with open(filename, "r") as file:
        get_tx = json.load(file)

        for e in get_tx:
            index_len = e["_source"]["layers"]["bitcoin"]["bitcoin.getblocktxn"]["bitcoin.getblocktxn.index_len"]
            count = int(index_len)

            i = 0
            list_index = []

            for i in range(count):
                list_index.insert(i,int(e["_source"]["layers"]["bitcoin"]["bitcoin.getblocktxn"]["Getblocktxn Index["+ str(i) +"]"]["bitcoin.getblocktxn.index"]))
                i += 1

            block_hash = e["_source"]["layers"]["bitcoin"]["bitcoin.getblocktxn"]["bitcoin.getblocktxn.block_hash"]
            r_block_hash = block_hash.replace(':','')
            hash_len = len(r_block_hash) - 1
            _id = ''

            while hash_len >= 0 :
                sub_data = ''
                sub_data = r_block_hash[hash_len-1] + r_block_hash[hash_len]
                _id += sub_data
                hash_len -= 2

            json_tx = {"_id": _id , "tx" : list_index}
            print(json_tx)
            collection.insert_one(json_tx)
            print('---------------------------------')

