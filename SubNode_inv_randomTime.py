# 전달 받은 inv 메시지간 사이 시간 (랜덤 지연 영향을 받음)

import pymongo
from pymongo import MongoClient
import json
import re
import time
import datetime
import numpy as np

#=======================================변수========================================#

# 정규식
pattern_received_inv = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\sinv\s\(\d+\sbytes\)\speer\=\d+)"
)


#=======================================함수========================================#

# 디버그 파일 열고 읽기
def open_debug_log():

    file = "\\\\210.125.29.157\\comnet\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정(코드, csv)\\코드\\sub_debug.log"
    f = open(file, "r") # 파일 열기
    f.seek(5)
    inv_time = []
    while True:
        line = f.readline()
        line = line.rstrip()
        if not line:
            break

        try:
            if pattern_received_inv.search(line):
                
                find_line = pattern_received_inv.search(line)
                receivedTime = change_dateTime(find_line.group('date'), find_line.group('time'))
                if receivedTime > datetime.datetime(2021,5,4,14,39,52) and receivedTime < datetime.datetime(2021,5,5,15,00,00):
                    inv_time.append(receivedTime)
                elif receivedTime > datetime.datetime(2021,5,5,15,00,00) :
                    break

        except Exception as ex:
            print("err : " + str(ex))
    f.close()

    random_time = []
    i = 0
    while i < len(inv_time) - 1:
        random_time.append(calculate_timeInterval(inv_time[i], inv_time[i+1]))
        i = i + 1

    # 평균
    print(np.average(random_time))
    # max
    print(np.max(random_time))
    # min
    print(np.min(random_time))
    # 중앙값
    print(np.median(random_time))

    random_time.sort(reverse=True)
    print("a")
    


# 시간 형변환
def change_dateTime(date, time):
    dateTime = datetime.datetime.strptime(date+" "+time, '%Y-%m-%d %H:%M:%S.%f')
    
    return dateTime

# 시간 계산
def calculate_timeInterval(startTime, endTime):
    timeInterval = (endTime - startTime).total_seconds()
    return timeInterval




#=======================================본문========================================#

open_debug_log()