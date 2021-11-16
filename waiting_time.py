# 블록 전달 받은 이후, 다시 전달하기까지 걸리는 시간 (queueing time)
# MainNode 용

import pymongo
from pymongo import MongoClient
import json
import re
import time
import datetime
import numpy as np

#=======================================변수========================================#
# 정규식
pattern_recvTime = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\scmpctblock\s\((?P<byte>\d+)\sbytes\)\speer\=(?P<peer>\d+))")
pattern_getHash = re.compile(r"Initialized\sPartiallyDownloadedBlock\sfor\sblock\s(?P<hash>\w+)\susing\sa\scmpctblock\sof\ssize\s(?P<byte>\d+)")
pattern_rectTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sSuccessfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s(?P<prefilled>\d+)\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s(?P<rtx>\d+)\stxn\srequested")
pattern_waitingTime = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(sending\scmpctblock\s\((?P<byte>\d+)\sbytes\)\speer\=(?P<peer>\d+))")
pattern_getHeight = re.compile(
    r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")

 # 컬렉션에 저장할 때 사용할 json 배열
block = {}

#=======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['blockpropagation']
    collection = mydb["waitingTime"]

    return collection

# 디버그 파일 열고 읽기
def open_debug_log(collection):
    global block

    get_recvTime = False
    get_hash = False
    get_rectTime = False
    get_waitingTime = False
    #
    file = "/root/.bitcoin/debug.log"
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
            if pattern_recvTime.search(line):
                find_line = pattern_recvTime.search(line)
                recv_time = change_dateTime(find_line.group('date'), find_line.group('time'))
                recv_peer = find_line.group('peer')
                cmpct_byte = find_line.group('byte')
                get_recvTime = True

            if pattern_getHash.search(line) and get_recvTime:
                find_line = pattern_getHash.search(line)
                if cmpct_byte == find_line.group('byte') :
                    cmpct_hash = find_line.group('hash')
                    get_hash = True

            if pattern_rectTime.search(line) and get_hash:
                find_line = pattern_rectTime.search(line)
                if find_line.group('hash') == cmpct_hash :
                    rect_time = change_dateTime(find_line.group('date'), find_line.group('time'))
                    get_rectTime = True

            if pattern_waitingTime.search(line) and get_rectTime:
                find_line = pattern_waitingTime.search(line)
                if find_line.group('byte') == cmpct_byte :
                    waiting_time = change_dateTime(find_line.group('date'), find_line.group('time'))
                    sending_peer = find_line.group('peer')
                    get_waitingTime = True

            if pattern_getHeight.search(line) and get_waitingTime:
                find_line = pattern_getHeight.search(line)
                if cmpct_hash == find_line.group('hash'):
                    block["_id"] = int(find_line.group('height'))
                    block["deliveryTime"] = calculate_timeInterval(recv_time, rect_time)
                    block["waitingTime"] = calculate_timeInterval(rect_time, waiting_time)
                    block["recvPeer"] = recv_peer
                    block["sendPeer"] = sending_peer
                    save_mongo_db(collection)

                    block = {}
                    get_recvTime = False
                    get_hash = False
                    get_rectTime = False
                    get_waitingTime = False

                    count = count + 1


        except Exception as ex:
            print("err : " + str(ex))


    f.close()

# 몽고 db에 저장
def save_mongo_db(collection):
    global block

    collection.insert_one(block)


# 시간 형변환
def change_dateTime(date, time):
    dateTime = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S.%f')

    return dateTime

# 시간 계산
def calculate_timeInterval(startTime, endTime):
    timeInterval = (endTime - startTime).total_seconds()
    return timeInterval


# 결과를 출력
def print_result(count):
    if count == 0:
        print("모든 데이터가 DB에 입력 완료된 상태입니다.")
    else :
        print("총 " + str(count) + "개를 DB에 저장하였습니다.")

#=======================================본문========================================#

collection = connect_monogoDB()
open_debug_log(collection)

