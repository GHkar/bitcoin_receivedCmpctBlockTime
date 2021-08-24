# 전달 받은 inv 메시지 트랜잭션과 전달 받은 ip
# cmpct block 메시지 사이
# blockheight의 기준은 cmpctblock을 받고 해당 블록의 이전에 받은 inv 메시지
# mainNode 용

import pymongo
from pymongo import MongoClient
import json
import re
import time
import datetime
import numpy as np

#=======================================변수========================================#

# 정규식
pattern_KAR_received_inv = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sKAR\'s\sLog\s:\sReceived\sInv\sgot\stx\=\s(?P<txOrwtx>\w+)\s(?P<hash>\w+)[,]\s(?P<haveOrnew>\w+)[,]\speer\=(?P<peerNum>\d+)[,]\sip\=(?P<ip>\d+[.]\d+[.]\d+[.]\d+[:]\d+)"
)
pattern_getHash = re.compile(
    r"Initialized\sPartiallyDownloadedBlock\sfor\sblock\s(?P<hash>\w+)\s(using\sa\scmpctblock\sof\ssize\s\d+)")

pattern_getHeight = re.compile(
    r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)"
)


# 값을 차례대로 얻기 위한 boolean
get_cmpctBlock = False
request_txCount = 0
request_tx_list = []
blockTxnPeer = -1

 # 컬렉션에 저장할 때 사용할 json 배열
block = {}
# 전역 변수
tx_index = 0

#=======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["log_MainNode_received_Inv"]
    
    return collection

def connect_monogoDB2():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["log_MainNode_peer_requestTx"]
    
    return collection

# 디버그 파일 열고 읽기
def open_debug_log(collection, collection2):
    global get_cmpctBlock

    global block
    global request_txCount
    global request_tx_list
    global blockTxnPeer
    global tx_index

    

    file = "\\\\210.125.29.157\\comnet\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정(코드, csv)\\코드\\main_debug.log"
    f = open(file, "r") # 파일 열기
    f.seek(5)
    # 필요 변수
    count = 0
    tx_inv = []
    take_data = collection2.find({})

    while True:
        line = f.readline()
        line = line.rstrip()
        if not line:
            print_result(count)
            break

        try:
            if pattern_KAR_received_inv.search(line):
                tx = {}
                find_line = pattern_KAR_received_inv.search(line)

                # inv에 포함된 트랜잭션
                tx["txid"] = find_line.group('hash')
                tx["txOrwtx"] = find_line.group('txOrwtx')
                tx["haveOrnew"] = find_line.group('haveOrnew')
                tx["peerNum"] = find_line.group('peerNum')
                tx["ip"] = find_line.group('ip')
                
                tx_inv.append(tx)

            # cmpctBlock
            if pattern_getHash.search(line) and not get_cmpctBlock:
                find_line = pattern_getHash.search(line)
                get_cmpctBlock = True
                cmpct_hash = find_line.group('hash')
            

            if pattern_getHeight.search(line) and get_cmpctBlock:
                find_line = pattern_getHeight.search(line)
                if cmpct_hash == find_line.group('hash'):
                    for peer in take_data[count]["peer"]:
                        tx_peer = []
                        for ti in tx_inv:
                            if ti["ip"] ==  peer["ip"]:
                                tx_peer.append(ti["txid"])
                        block["_id"] = find_line.group('height') + peer["peerNum"]
                        block["height"] = int(find_line.group('height'))
                        block["blockHash"] = cmpct_hash
                        block["peer"] = peer["ip"]
                        block["invTx"] = tx_peer
                        
                        save_mongo_db(collection)
                        reset_value()
                    
                    tx_inv = []
                    count = count + 1
                

        except Exception as ex:
            print("err : " + str(ex))
            reset_value()

    
    f.close()

# 몽고 db에 저장
def save_mongo_db(collection):
    global block

    collection.insert_one(block)

# 시간 형변환
def change_dateTime(date, time):
    dateTime = datetime.datetime.strptime(date+" "+time, '%Y-%m-%d %H:%M:%S.%f')
    
    return dateTime

# 시간 계산
def calculate_timeInterval(startTime, endTime):
    timeInterval = (endTime - startTime).total_seconds()
    return timeInterval




# 다시 false로 변환, 값 초기화
def reset_value():
    global get_cmpctBlock
    global getBlockTxn
    global request_txCount
    global request_tx_list
    global blockTxnPeer

    global block
    global tx_index
    
    get_cmpctBlock = False
    getBlockTxn = False

    block = {}
    request_txCount = 0
    request_tx_list = []
    blockTxnPeer = -1
    tx_index = 0


# 결과를 출력
def print_result(count):
    if count == 0:
        print("모든 데이터가 DB에 입력 완료된 상태입니다.")
    else :
        print("총 " + str(count) + "개를 DB에 저장하였습니다.")

#=======================================본문========================================#

collection = connect_monogoDB()
open_debug_log(collection, connect_monogoDB2())