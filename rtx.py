# 요청한 트랜잭션 리스트 저장
# SubNode 용

import pymongo
from pymongo import MongoClient
import json
import re
import time
import datetime
import numpy as np

#=======================================변수========================================#
# 정규식
pattern_endTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sSuccessfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s(?P<prefilled>\d+)\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s(?P<rtx>\d+)\stxn\srequested")
pattern_getHeight = re.compile(
    r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")

 # 컬렉션에 저장할 때 사용할 json 배열
block = {}

#=======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection = mydb["50-1requestTxn"]

    return collection

# 디버그 파일 열고 읽기
def open_debug_log(collection):
    global block

    passbool = False
    #
    file = "debug.log"
    f = open(file, "r") # 파일 열기
    f.seek(5)
    # 필요 변수
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
                # if time_1 > datetime.datetime(2021,6,22,15,32,43) and time_1 < datetime.datetime(2021,6,24,5,46,9): # 6월 23일
                #     passbool = True
                # if time_1 > datetime.datetime(2021,6,24,5,46,8):
                #     print_result(count)
                #     break
                #if time_1 > datetime.datetime(2021,6,27,14,3,50) and time_1 < datetime.datetime(2021,6,29,10,51,8): # 6월 27일

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

# 몽고 db에 저장
def save_mongo_db(collection):
    global block

    collection.insert_one(block)

#
# # 시간 형변환
# def change_dateTime(date, time):
#     dateTime = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S.%f')
#
#     return dateTime

# 결과를 출력
def print_result(count):
    if count == 0:
        print("모든 데이터가 DB에 입력 완료된 상태입니다.")
    else :
        print("총 " + str(count) + "개를 DB에 저장하였습니다.")

#=======================================본문========================================#

collection = connect_monogoDB()
open_debug_log(collection)

