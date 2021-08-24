import pymongo
from pymongo import MongoClient
import json
import re
import datetime

# =======================================변수========================================#

# 정규식
pattern_startTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\scmpctblock\s\(\d+\sbytes\)\speer\=\d+)")
pattern_getHash = re.compile(
    r"Initialized\sPartiallyDownloadedBlock\sfor\sblock\s(?P<hash>\w+)\s(using\sa\scmpctblock\sof\ssize\s\d+)")
pattern_endTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sSuccessfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s\d+\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s\d+\stxn\srequested")
pattern_getHeight = re.compile(
    r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")

# 값을 차례대로 얻기 위한 boolean
get_startTime = False
get_endTime = False
get_height = False
get_hash = False

# 컬렉션에 저장할 때 사용할 json 배열
db_json = {}


# =======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://ip:portnum/")
    mydb = myclient['DB 이름']
    collection = mydb["컬렉션 이름"]
    reset_nowPos(collection)

    return collection


# 디버그 파일 열고 읽기
def open_debug_log(collection):
    # 전역 변수 사용
    global get_startTime
    global get_endTime
    global get_height
    global get_hash
    global db_json

    count = 0  # 총 몇 개를 넣었는지 출력

    f = open("debug.log", "r")  # 파일 열기
    readPos = load_nowPos()
    if readPos == 0:
        f.seek(5)  # 처음 여는 파일, 앞 공백 무시
    else:
        f.seek(readPos)  # 읽었던 위치 부터 읽기

    # 라인 읽기 및 비교와 데이터 추출
    while True:
        line = f.readline()
        line = line.rstrip()
        if not line: break  # 라인이 아니라면 종료

        try:
            if pattern_startTime.search(line) and not get_startTime:
                find_line = pattern_startTime.search(line)
                startTime = change_dateTime(find_line.group('date'), find_line.group('time'))
                get_startTime = True

            if pattern_getHash.search(line) and get_startTime and not get_hash:
                find_line = pattern_getHash.search(line)
                cmpct_hash = find_line.group('hash')
                get_hash = True

            if pattern_endTime.search(line) and get_startTime:
                find_line = pattern_endTime.search(line)
                if cmpct_hash == find_line.group('hash'):
                    endTime = change_dateTime(find_line.group('date'), find_line.group('time'))
                    get_endTime = True

            if pattern_getHeight.search(line) and get_hash:
                find_line = pattern_getHeight.search(line)
                if cmpct_hash == find_line.group('hash'):
                    cmpct_height = int(find_line.group('height'))
                    get_height = True

            if get_startTime and get_endTime and get_height:
                receiveTime = calculate_timeInterval(startTime, endTime)
                make_db_json(cmpct_height, startTime, endTime, receiveTime, cmpct_hash)
                save_mongo_db(collection)
                reset_value()
                count = count + 1
                db_json = {}

        except Exception as ex:
            print("err : " + str(ex))
            reset_value()
            db_json = {}

    nowPos = f.tell()
    save_nowPos(nowPos)
    print_result(count)
    f.close()


# 몽고 db에 저장
def save_mongo_db(collection):
    global db_json

    collection.insert_one(db_json)


# 시간 형변환
def change_dateTime(date, time):
    dateTime = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S.%f')

    return dateTime


# 시간 계산
def calculate_timeInterval(startTime, endTime):
    timeInterval = (endTime - startTime).total_seconds()
    return timeInterval


# json 파일로 DB에 넣을 정보 저장
def make_db_json(height, startTime, endTime, receiveTime, hash):
    global db_json

    db_json['_id'] = height
    db_json['startTime'] = startTime
    db_json['endTime'] = endTime
    db_json['receiveTime_result'] = receiveTime
    db_json['hash'] = hash


# 파일 읽은 위치 저장
def save_nowPos(pos):
    f = open("nowPos.txt", "r+")
    f.write(str(pos))
    f.close()


# 파일 읽은 위치 로드
def load_nowPos():
    f = open("nowPos.txt", "r")
    readPos = int(f.readline().rstrip())
    f.close()

    return readPos


# 컬렉션 없을 시에 nowPos 초기화
def reset_nowPos(collection):
    if collection.estimated_document_count() == 0:  # 컬렉션 내의 갯수를 세는 함수
        f = open("nowPos.txt", "r+")
        f.write("0")
        f.close()


# 다시 false로 변환, 값 초기화
def reset_value():
    global get_startTime
    global get_endTime
    global get_height
    global get_hash

    get_startTime = False
    get_endTime = False
    get_height = False
    get_hash = False


# 결과를 출력
def print_result(count):
    if count == 0:
        print("모든 데이터가 DB에 입력 완료된 상태입니다.")
    else:
        print("총 " + str(count) + "개를 DB에 저장하였습니다.")


# =======================================본문========================================#

collection = connect_monogoDB()
open_debug_log(collection)

