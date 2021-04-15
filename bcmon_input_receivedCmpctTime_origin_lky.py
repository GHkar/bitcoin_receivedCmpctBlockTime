import pymongo
from pymongo import MongoClient
import json
import time
import datetime

def text_to_date(text_in):
    temp_date = text_in[0:10].split("-")
    temp_time = text_in[11:-1].split(":")
    temp_sec = temp_time[2].split(".")
    temp_all_time = datetime.datetime(int(temp_date[0]),int(temp_date[1]),int(temp_date[2]),int(temp_time[0]),int(temp_time[1]),int(temp_sec[0]), int(temp_sec[1]))
    return temp_all_time

def cmpctblock_ver_time():
    myclient = pymongo.MongoClient("mongodb://210.125.29.155:10001/")
    mydb = myclient["bitcoin"]
    collection = mydb["GRAPH_cmpctblock_received_time_per_height"]
    f = open("debug.log", "r")
    load_hash = ""
    rc_flag = False
    rb_flag = False
    db_json = {}
    while True:
        line = f.readline()
        if not line: #break
            time.sleep(60*60)
            continue
        log_line = line.split(' ')
        try:
            if (log_line[1] == "received:") and (log_line[2] == "cmpctblock") and rc_flag == False:
                rc_time = text_to_date(log_line[0])
                rc_peer = log_line[5]
            if (log_line[1] == "Initialized"):
                rci_hash = log_line[5]
                rc_flag = True
            if (log_line[1] == "Successfully") and (log_line[2] == "reconstructed"):
                rb_time = text_to_date(log_line[0])
                rb_flag = True
            if log_line[1] == "UpdateTip:":
                if rb_flag == True:
                    bheight = log_line[4][7:]
                    up_time = (rb_time - rc_time).total_seconds()
                    db_json['_id'] = int(bheight)
                    db_json['received_time'] = up_time
                    collection.insert_one(db_json)
                    db_json = {}
                    rc_flag = False
                    rb_flag = False
                
        except Exception as ex:
            print("err : " + str(ex))
    f.close()

cmpctblock_ver_time()

