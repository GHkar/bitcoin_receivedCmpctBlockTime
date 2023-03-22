import pymongo
from pymongo import MongoClient
import json
import re
import datetime

#=======================================변수========================================#

# 정규식
pattern_startTime = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\scmpctblock\s\(\d+\sbytes\)\speer\=\d+)")
pattern_getHash = re.compile(r"Initialized\sPartiallyDownloadedBlock\sfor\sblock\s(?P<hash>\w+)\s(using\sa\scmpctblock\sof\ssize\s\d+)")
pattern_endTime = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sSuccessfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s\d+\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s\d+\stxn\srequested")
pattern_getHeight = re.compile(r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")
pattern_getblocktxn = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\ssending\sgetblocktxn\s\(\d+\sbytes\)\speer=\d+")
pattern_blocktxn = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sreceived[:]\sblocktxn\s\(\d+\sbytes\)\speer=\d+")

# 값을 차례대로 얻기 위한 boolean
get_startTime = False
get_endTime = False
get_height = False
get_hash = False
get_getblocktxn = False

 # 컬렉션에 저장할 때 사용할 json 배열
db_json = {}

#=======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['test']
    collection = mydb["getblocktxn"]

    return collection

# 디버그 파일 열고 읽기
def open_debug_log(collection):
    global get_startTime
    global get_endTime
    global get_height
    global get_hash
    global get_getblocktxn
    global db_json

    count = 0  # 총 몇 개를 넣었는지 출력

    f = open("xad", "r") # 파일 열기
    #f.seek(5)  # 처음 여는 파일, 앞 공백 무시

    # 라인 읽기 및 비교와 데이터 추출
    while True:
        line = f.readline()
        line = line.rstrip()
        if not line: break # 라인이 아니라면 종료

        try:
            if pattern_startTime.search(line) and not get_startTime:
                find_line = pattern_startTime.search(line)
                startTime = change_dateTime(find_line.group('date'), find_line.group('time'))
                get_startTime = True

            if pattern_getHash.search(line) and get_startTime and not get_hash:
                find_line = pattern_getHash.search(line)
                cmpct_hash = find_line.group('hash')
                get_hash = True

            if pattern_getblocktxn.search(line) and get_hash and not get_getblocktxn:
                find_line = pattern_getblocktxn.search(line)
                getbtx_time = change_dateTime(find_line.group('date'), find_line.group('time'))
                get_getblocktxn = True

            if pattern_blocktxn.search(line) and get_getblocktxn :
                find_line = pattern_blocktxn.search(line)
                btx_time = change_dateTime(find_line.group('date'), find_line.group('time'))

            if pattern_endTime.search(line) and get_hash:
                find_line = pattern_endTime.search(line)
                if cmpct_hash == find_line.group('hash'):
                    endTime = change_dateTime(find_line.group('date'), find_line.group('time'))
                    get_endTime = True

            if pattern_getHeight.search(line) and get_endTime:
                find_line = pattern_getHeight.search(line)
                if cmpct_hash == find_line.group('hash'):
                    cmpct_height = int(find_line.group('height'))
                    get_height = True

            if get_startTime and get_endTime and get_height:
                receiveTime = calculate_timeInterval(startTime, endTime)
                
                # getblocktxn을 주고받지 않았다면
                if not get_getblocktxn :
                    getblocktxnTime = 0
                    blocktxnTime = 0
                    reconstructedTime = 0
                else :
                    getblocktxnTime = calculate_timeInterval(startTime, getbtx_time)
                    blocktxnTime = calculate_timeInterval(getbtx_time, btx_time)
                    reconstructedTime = calculate_timeInterval(btx_time, endTime)

                make_db_json(cmpct_height, startTime, endTime, receiveTime, getblocktxnTime, blocktxnTime, reconstructedTime, cmpct_hash)
                save_mongo_db(collection)
                reset_value()
                count = count + 1
                db_json = {}

        except Exception as ex:
            print("err : " + str(ex))
            reset_value()
            db_json = {}

    print_result(count)
    f.close()

# 몽고 db에 저장
def save_mongo_db(collection):
    global db_json

    collection.insert_one(db_json)

# 시간 형변환
def change_dateTime(date, time):
    dateTime = datetime.datetime.strptime(date+" "+time, '%Y-%m-%d %H:%M:%S.%f')

    return dateTime

# 시간 계산
def calculate_timeInterval(startTime, endTime):
    timeInterval = (endTime - startTime).total_seconds()
    return timeInterval

# json 파일로 DB에 넣을 정보 저장
def make_db_json(height, startTime, endTime, receiveTime, getblocktxnTime, blocktxnTime, reconstructedTime, hash):
    global db_json

    db_json['_id'] = height
    db_json['startTime'] = startTime
    db_json['endTime'] = endTime
    db_json['receiveTime_result'] = receiveTime
    db_json['getblocktxnTime'] = getblocktxnTime
    db_json['blocktxnTime'] = blocktxnTime
    db_json['reconstructedTime'] = reconstructedTime
    db_json['hash'] = hash


# 다시 false로 변환, 값 초기화
def reset_value():
    global get_startTime
    global get_endTime
    global get_height
    global get_hash
    global get_getblocktxn

    get_startTime = False
    get_endTime = False
    get_height = False
    get_hash = False
    get_getblocktxn = False

# 결과를 출력
def print_result(count):
    if count == 0:
        print("모든 데이터가 DB에 입력 완료된 상태입니다.")
    else :
        print("총 " + str(count) + "개를 DB에 저장하였습니다.")

#=======================================본문========================================#

collection = connect_monogoDB()
open_debug_log(collection)

