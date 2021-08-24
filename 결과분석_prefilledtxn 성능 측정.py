import pymongo
from pymongo import MongoClient
import json
import re
import datetime

#=======================================변수========================================#

# 정규식
pattern_1 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sStart)")
pattern_2 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sLoad\sTxInfo\s\d+)")
pattern_3 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sMake\sindexVector)")
pattern_4 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sSorting\sDescending)")
pattern_5 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sPrefilledTxn)")
pattern_6 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sSorting\sprefilledtxn)")
pattern_7 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sChange\sindex)")
pattern_8 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sMake\sShortids)")
pattern_9 = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(KAR\'s\sLog\sShortids\ssize\s\d+)")
pattern_getHeight = re.compile(r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")


# 컬렉션에 저장할 때 사용할 json 배열
db_json = {}
#=======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['prefilledtxn']
    collection = mydb["check_performance_per_phase"]
    
    return collection

def checkTime(collection):
    global db_json
    count = 0

    #file = "\\\\210.125.29.157\\comnet\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정(코드, csv)\\코드\\mdpi\\debug.log"
    f = open("debug.log", "r") # 파일 열기
    f.seek(5)

    passbool = False

    while True:
        line = f.readline()
        line = line.rstrip()
        if not line:
            print_result(count)
            print(f.tell())
            break 

        try:
            if pattern_1.search(line) :
                find_line = pattern_1.search(line)
                time_1 = change_dateTime(find_line.group('date'), find_line.group('time'))
                passbool = True
            
            if pattern_2.search(line) and passbool:
                find_line = pattern_2.search(line)
                time_2 = change_dateTime(find_line.group('date'), find_line.group('time'))

            if pattern_3.search(line) and passbool:
                find_line = pattern_3.search(line)
                time_3 = change_dateTime(find_line.group('date'), find_line.group('time'))

            if pattern_4.search(line) and passbool:
                find_line = pattern_4.search(line)
                time_4 = change_dateTime(find_line.group('date'), find_line.group('time'))

            if pattern_5.search(line) and passbool:
                find_line = pattern_5.search(line)
                time_5 = change_dateTime(find_line.group('date'), find_line.group('time'))
            
            if pattern_6.search(line) and passbool:
                find_line = pattern_6.search(line)
                time_6 = change_dateTime(find_line.group('date'), find_line.group('time'))

            if pattern_7.search(line) and passbool:
                find_line = pattern_7.search(line)
                time_7 = change_dateTime(find_line.group('date'), find_line.group('time'))

            if pattern_8.search(line) and passbool:
                find_line = pattern_8.search(line)
                time_8 = change_dateTime(find_line.group('date'), find_line.group('time'))

            if pattern_9.search(line) and passbool:
                find_line = pattern_9.search(line)
                time_9 = change_dateTime(find_line.group('date'), find_line.group('time'))
            
            if pattern_getHeight.search(line) and passbool:
                find_line = pattern_getHeight.search(line)
                cmpctheight = find_line.group('height')

                time_list = make_time(time_1, time_2, time_3, time_4, time_5, time_6, time_7, time_8, time_9)
                make_db_json(cmpctheight, time_list)
                save_mongo_db(collection)
                count = count + 1
                passbool = False
                db_json = {}

        except Exception as ex:
            print("err : " + str(ex))
            passbool = False
            db_json = {}

def make_time(t1, t2, t3, t4, t5, t6, t7, t8, t9):
    time_list = []
    time_list.append(calculate_timeInterval(t1, t2))
    time_list.append(calculate_timeInterval(t2, t3))
    time_list.append(calculate_timeInterval(t3, t4))
    time_list.append(calculate_timeInterval(t4, t5))
    time_list.append(calculate_timeInterval(t5, t6))
    time_list.append(calculate_timeInterval(t6, t7))
    time_list.append(calculate_timeInterval(t7, t8))
    time_list.append(calculate_timeInterval(t8, t9))

    return time_list

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
    return format(timeInterval, '.20f')


# json 파일로 DB에 넣을 정보 저장
def make_db_json(height, time_list):
    global db_json

    db_json['_id'] = height
    db_json['preparing'] = time_list[0]
    db_json['readingMempool'] = time_list[1]
    db_json['indexing'] = time_list[2]
    db_json['ordering'] = time_list[3]
    db_json['fillingprefilled'] = time_list[4]
    db_json['orderingindex'] = time_list[5]
    db_json['changeindex'] = time_list[6]
    db_json['makingshortids'] = time_list[7]

# 결과를 출력
def print_result(count):
    if count == 0:
        print("모든 데이터가 DB에 입력 완료된 상태입니다.")
    else :
        print("총 " + str(count) + "개를 DB에 저장하였습니다.")


#=======================================본문========================================#

collection = connect_monogoDB()
checkTime(collection)