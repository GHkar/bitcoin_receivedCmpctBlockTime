# ▒~Z~T청▒~U~\ ▒~J▒▒~^~\▒~^▒▒~E~X 리▒~J▒▒~J▒ ▒| ~@▒~^▒
# SubNode ▒~Z▒

import pymongo
from pymongo import MongoClient
import json
import re
import time
import datetime
import numpy as np

#=======================================▒~@▒~H~X========================================#
# ▒| ~U▒~\▒~K~]
pattern_endTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sSuccessfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s(?P<prefilled>\d+)\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s(?P<rtx>\d+)\stxn\srequested")
pattern_getHeight = re.compile(
    r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")

 # 컬▒| ~I▒~E~X▒~W~P ▒| ~@▒~^▒▒~U|  ▒~U~L ▒~B▒▒~Z▒▒~U|  json 배▒~W▒
block = {}

#=======================================▒~U▒▒~H~X========================================#

# 몽▒|  db▒~W~P ▒~W▒결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection = mydb["50-1requestTxn"]

    return collection

# ▒~T~T▒~D그 ▒~L~L▒~]▒ ▒~W▒▒|  ▒~]▒기
def open_debug_log(collection):
    global block

    passbool = False
    #
    file = "debug.log"
    f = open(file, "r") # ▒~L~L▒~]▒ ▒~W▒기
    f.seek(5)
    # ▒~U~D▒~Z~T ▒~@▒~H~X
    count = 0

    while True:
        line = f.readline()
        line = line.rstrip()
        if not line:
            print_result(count)
            print(f.tell())
            break

        try:
            if pattern_endTime.search(line):
                find_line = pattern_endTime.search(line)
                #time_1 = change_dateTime(find_line.group('date'), find_line.group('time'))
                cmpct_hash = find_line.group('hash')
                rtx = find_line.group('rtx')
                passbool = True
                # if time_1 > datetime.datetime(2021,6,22,15,32,43) and time_1 < datetime.datetime(2021,6,24,5,46,9): # 6▒~[~T 23▒~]▒
                #     passbool = True
                # if time_1 > datetime.datetime(2021,6,24,5,46,8):
                #     print_result(count)
                #     break
                #if time_1 > datetime.datetime(2021,6,27,14,3,50) and time_1 < datetime.datetime(2021,6,29,10,51,8): # 6▒~[~T 27▒~]▒

            if pattern_getHeight.search(line) and passbool:
                find_line = pattern_getHeight.search(line)
                if cmpct_hash == find_line.group('hash'):
                    block["_id"] = int(find_line.group('height'))
                    block["requestTx"] = int(rtx)
                    save_mongo_db(collection)

                    block = {}

                    count = count + 1


        except Exception as ex:
            print("err : " + str(ex))


    f.close()

# 몽▒|  db▒~W~P ▒| ~@▒~^▒
def save_mongo_db(collection):
    global block

    collection.insert_one(block)

#
# # ▒~K~\▒~D ▒~X~U▒~@▒~Y~X
# def change_dateTime(date, time):
#     dateTime = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S.%f')
#
#     return dateTime

# 결과를 ▒~\▒| ▒
def print_result(count):
    if count == 0:
        print("모▒~S|  ▒~M▒▒~]▒▒~D▒▒~@ DB▒~W~P ▒~^~E▒| ▒ ▒~Y~D▒~L▒~P~\ ▒~C~A▒~C~\▒~^~E▒~K~H▒~K▒.")
    else :
        print("▒~] " + str(count) + "▒~\를 DB▒~W~P ▒| ~@▒~^▒▒~U~X▒~X~@▒~J▒▒~K~H▒~K▒.")

#=======================================본문========================================#

collection = connect_monogoDB()
open_debug_log(collection)



