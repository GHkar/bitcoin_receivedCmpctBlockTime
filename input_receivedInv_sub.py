# 전달 받은 inv 메시지 트랜잭션과 전달 받은 ip
# cmpct block 메시지 사이
# 전달 받은 inv 메시지에 대한 getdata 메시지를 주고 transaction 데이터를 받았는지 여부 확인 필요
# blockheight의 기준은 cmpctblock을 받고 해당 블록의 이전에 받은 inv 메시지
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
pattern_received_cmpctBlock = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\scmpctblock\s\(\d+\sbytes\)\speer\=\d+)"
)
pattern_received_inv = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\sinv\s\(\d+\sbytes\)\speer\=\d+)"
)
pattern_KAR_received_inv = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sKAR\'s\sLog\s:\sReceived\sInv\sgot\stx\=\s(?P<txOrwtx>\w+)\s(?P<hash>\w+)[,]\s(?P<haveOrnew>\w+)[,]\speer\=(?P<peerNum>\d+)[,]\sip\=(?P<ip>\d+[.]\d+[.]\d+[.]\d+[:]\d+)"
)
pattern_requesting_tx = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(Requesting\s(?P<txOrwtx>\w+)\s(?P<hash>\w+)\speer\=\d+)"
)
pattern_acceptToMempool = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(AcceptToMemoryPool:\speer\=\d+:\s(?P<isAccept>\w+)\s(?P<hash>\w+)\s\(poolsz\s(?P<mempoolTxNum>\d+)\stxn[,]\s(?P<mempoolSize>\d+)\skB)"
)
pattern_acceptOrphanTx = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s\s\s\saccepted\sorphan\stx\s(?P<hash>\w+)"
)
pattern_blockHash = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sSuccessfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s\d+\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s\d+\stxn\srequested"
)
pattern_getHeight = re.compile(
    r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)"
)
pattern_KAR_send_getBlockTxn = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sKAR\'s\sLog\s:\sSending\sgetBlockTxn\sindex\=(?P<index>(\d+\s)+)[,]\sblock\=(?P<blockHash>\w+)"
)
pattern_KAR_received_blockTxn = re.compile(
  r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sKAR\'s\sLog\s:\sReceived\sblockTxn\stx\=(?P<hash>\w+)[,]\sblock\=(?P<blockHash>\w+)[,]\speer\=(?P<peer>\d+)"
)

# 값을 차례대로 얻기 위한 boolean
get_cmpctBlock = False
get_inv = False
get_requestingTx = False # True 면 inv 메시지가 끝
start_inv = False
get_hash = False
getBlockTxn = False
request_txCount = 0
request_tx_list = []
blockTxnPeer = -1

 # 컬렉션에 저장할 때 사용할 json 배열
block = {}
block["inv_list"] = []
# 전역 변수
inv_count = 0
tx_index = 0

#=======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.29.230:80/")
    mydb = myclient['bitcoin']
    collection = mydb["log_SubNode_received_Inv"]
    
    return collection

# 디버그 파일 열고 읽기
def open_debug_log(collection):
    global get_cmpctBlock
    global get_inv
    global get_requestingTx
    global start_inv
    global get_hash
    global getBlockTxn

    global block
    global inv_count
    global request_txCount
    global request_tx_list
    global blockTxnPeer
    global tx_index

    file = "\\\\210.125.29.157\\comnet\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정(코드, csv)\\코드\\debug.log"
    f = open(file, "r") # 파일 열기
    f.seek(5)
    # 필요 변수
    count = 0
    inv = {}

    while True:
        line = f.readline()
        line = line.rstrip()
        if not line:
            print_result(count)
            break

        try:
            if pattern_received_inv.search(line) and not get_inv:
                if get_requestingTx:
                    block["inv_list"].append(inv)
                    inv = {}
                    get_requestingTx = False
                    inv_count = inv_count + 1
                
                find_line = pattern_received_inv.search(line)
                receivedTime = change_dateTime(find_line.group('date'), find_line.group('time'))
                if receivedTime > datetime.datetime(2021,5,4,14,39,52) and receivedTime < datetime.datetime(2021,5,5,15,00,00):
                    get_inv = True
                elif receivedTime > datetime.datetime(2021,5,5,15,00,00) :
                    print_result(count)
                    break
                    
            if pattern_KAR_received_inv.search(line) and get_inv:
                tx = {}
                find_line = pattern_KAR_received_inv.search(line)
                # inv 메시지에 포함된 트랜잭션 하나에 대한 정보
                if not start_inv:
                    inv["peerNum"] = find_line.group('peerNum')
                    inv["ip"] = find_line.group('ip')
                    inv["tx_list"] = []
                    inv["acceptMempoolTx"] = []
                    inv["txCount"] = 0
                    inv["acceptMempoolTxCount"] = 0
                    start_inv = True
                # inv에 포함된 트랜잭션
                tx["txid"] = find_line.group('hash')
                tx["txOrwtx"] = find_line.group('txOrwtx')
                tx["haveOrnew"] = find_line.group('haveOrnew')

                inv["tx_list"].append(tx)
                inv["txCount"] = inv["txCount"] + 1
                    
            # inv 메시지의 끝
            if pattern_requesting_tx.search(line) and start_inv:
                get_inv = False
                start_inv = False
                get_requestingTx = True

            # inv 로 받은 tx에서 getdata를 통해 tx를 다 받았는지 확인
            if pattern_acceptToMempool.search(line) and get_requestingTx:
                find_line = pattern_acceptToMempool.search(line)
                inv["acceptMempoolTx"].append(find_line.group('hash'))
                inv["acceptMempoolTxCount"] = inv["acceptMempoolTxCount"] + 1

            if pattern_acceptOrphanTx.search(line) and get_requestingTx:
                find_line = pattern_acceptOrphanTx.search(line)
                inv["acceptMempoolTx"].append(find_line.group('hash'))
                inv["acceptMempoolTxCount"] = inv["acceptMempoolTxCount"] + 1

            # cmpctBlock
            if pattern_received_cmpctBlock.search(line) and not get_cmpctBlock:
                find_line = pattern_received_cmpctBlock.search(line)
                receivedTime = change_dateTime(find_line.group('date'), find_line.group('time'))
                if receivedTime > datetime.datetime(2021,5,4,15,00,00) and receivedTime < datetime.datetime(2021,5,5,15,00,00):
                    get_cmpctBlock = True
            
            # getblockTxn
            if pattern_KAR_send_getBlockTxn.search(line) and get_cmpctBlock:
                find_line = pattern_KAR_send_getBlockTxn.search(line)
                index_str = find_line.group('index')
                index_list = list(map(int,index_str[:-1].split(' ')))
                request_txCount = len(index_list)
                cmpct_hash = find_line.group('blockHash')
                getBlockTxn = True

            # blocktxn
            if pattern_KAR_received_blockTxn.search(line) and get_cmpctBlock and getBlockTxn:
                find_line = pattern_KAR_received_blockTxn.search(line)
                rtx = {}
                if cmpct_hash == find_line.group('blockHash'):
                    rtx["index"] = index_list[tx_index]
                    rtx["txid"] = find_line.group('hash')
                    request_tx_list.append(rtx)
                    tx_index = tx_index+1
                blockTxnPeer = find_line.group('peer')

            if pattern_blockHash.search(line) and get_cmpctBlock:
                find_line = pattern_blockHash.search(line)
                if not getBlockTxn :
                    cmpct_hash = find_line.group('hash')
                if cmpct_hash == find_line.group('hash'):
                    get_hash = True

            if pattern_getHeight.search(line) and get_hash:
                find_line = pattern_getHeight.search(line)
                if cmpct_hash == find_line.group('hash'):
                    block["_id"] = int(find_line.group('height'))
                    block["blockHash"] = cmpct_hash
                    block["invCount"] = inv_count
                    block["requestTxCount"] = request_txCount
                    block["requestTx"] = request_tx_list
                    block["receivedBlockTxnPeer"] = blockTxnPeer
                    save_mongo_db(collection)
                    reset_value()

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
    global get_inv
    global get_requestingTx
    global start_inv
    global get_hash
    global getBlockTxn
    global request_txCount
    global request_tx_list
    global blockTxnPeer

    global block
    global inv_count
    global tx_index
    

    get_cmpctBlock = False
    get_inv = False
    get_requestingTx = False # True 면 inv 메시지가 끝
    start_inv = False
    get_hash = False
    getBlockTxn = False

    block = {}
    block["inv_list"] = []
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
open_debug_log(collection)