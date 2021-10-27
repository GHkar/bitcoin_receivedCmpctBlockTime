import json

import re

import time

from datetime import datetime

import sys

sys.path.insert(0, './')

from time_utils import *

from connect_utils import *


#=======================================변수========================================#


# 정규식

pattern_startTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\scmpctblock\s\(\d+\sbytes\)\speer\=\d+)")

pattern_getHash = re.compile(
    r"Initialized\sPartiallyDownloadedBlock\sfor\sblock\s(?P<hash>\w+)\s(using\sa\scmpctblock\sof\ssize\s\d+)")

pattern_endTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(Successfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s\d+\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s\d+\stxn\srequested)")

pattern_getHeight = re.compile(
    r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")

pattern_getblocktxn = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\ssending\sgetblocktxn\s\(\d+\sbytes\)\speer=\d+")

pattern_blocktxn = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sreceived[:]\sblocktxn\s\(\d+\sbytes\)\speer=\d+")


# 그냥  recieved block만 했을 때

pattern_block_startTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sreceived\sblock\s(?P<hash>\w+)\speer\=\d+")

pattern_block_getHeight = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sUpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")


# 값을 차례대로 얻기 위한 boolean

get_startTime = False

get_endTime = False

get_height = False

get_hash = False

get_getblocktxn = False


get_block_startTime = False

get_block_height = False


is_cmpctBlock = False


# 컬렉션에 저장할 때 사용할 json 배열

db_json = {}


#=======================================함수========================================#

# debug log read and write

def open_debug_log(mycol, stored_id):

   global get_startTime

   global get_endTime

   global get_height

   global get_hash

   global get_block_height

   global get_block_startTime

   global is_cmpctBlock

   global get_getblocktxn

   global db_json


# 라인 읽기 및 비교와 데이터 추출

   while True:

      mydoc = mycol.find_one({"_id": stored_id}, {"_id": 0, "log": 1})

      if mydoc is None or mydoc is None:

         time.sleep(86400)

      else:

         line = str(mydoc['log'])

         line = line.rstrip()

         try:

            if pattern_startTime.search(line) and not get_startTime:

               find_line = pattern_startTime.search(line)

               startTime = change_dateTime(
                   find_line.group('date'), find_line.group('time'))

               get_startTime = True

               is_cmpctBlock = True

            elif pattern_block_startTime.search(line) and not get_block_startTime:

               find_line = pattern_block_startTime.search(line)

               cmpct_hash = find_line.group('hash')

               startTime = change_dateTime(
                   find_line.group('date'), find_line.group('time'))

               get_block_startTime = True

               is_cmpctBlock = False

            if is_cmpctBlock:

               if pattern_getHash.search(line) and get_startTime and not get_hash:

                  find_line = pattern_getHash.search(line)

                  cmpct_hash = find_line.group('hash')

                  get_hash = True

               if pattern_getblocktxn.search(line) and get_hash and not get_getblocktxn:

                  find_line = pattern_getblocktxn.search(line)

                  getbtx_time = change_dateTime(
                      find_line.group('date'), find_line.group('time'))

                  get_getblocktxn = True

                  gs_id = stored_id

               if pattern_blocktxn.search(line) and get_getblocktxn:

                  find_line = pattern_blocktxn.search(line)

                  btx_time = change_dateTime(
                      find_line.group('date'), find_line.group('time'))

                  bs_id = stored_id

               if pattern_endTime.search(line) and get_startTime:

                  find_line = pattern_endTime.search(line)

                  if cmpct_hash == find_line.group('hash'):

                     endTime = change_dateTime(find_line.group(
                         'date'), find_line.group('time'))

                     get_endTime = True

                     res_id = stored_id

               if pattern_getHeight.search(line) and get_hash:

                  find_line = pattern_getHeight.search(line)

                  if cmpct_hash == find_line.group('hash'):

                     cmpct_height = int(find_line.group('height'))

                     get_height = True

               if get_startTime and get_endTime and get_height:

                  receiveTime = calculate_timeInterval(startTime, endTime)

                  # getblocktxn을 주고받지 않았다면

                  if not get_getblocktxn:
                     getblocktxnTime = 0
                     blocktxnTime = 0
                     reconstructedTime = 0
                     res_id = 0
                     bs_id = 0
                     gs_id = 0

                  else :

                     getblocktxnTime = calculate_timeInterval(startTime, getbtx_time)

                     blocktxnTime = calculate_timeInterval(getbtx_time, btx_time)

                     reconstructedTime = calculate_timeInterval(btx_time, endTime)

          

                  make_db_json_cmpctblock(cmpct_height, receiveTime, stored_id, getblocktxnTime, gs_id, blocktxnTime, bs_id, reconstructedTime, res_id, startTime.strftime("%Y-%m-%d %H:%M:%S.%f"))

                  print(db_json)

                  reset_value()

                  save_maria_anl_db()

                  db_json = {}

            else:

               if pattern_block_getHeight.search(line) and get_block_startTime:

                  find_line = pattern_block_getHeight.search(line)

                  if cmpct_hash == find_line.group('hash'):

                     cmpct_height = int(find_line.group('height'))

                     endTime = change_dateTime(find_line.group('date'), find_line.group('time'))

                     get_block_height = True

                  

               if get_block_startTime and get_block_height:

                  receiveTime = calculate_timeInterval(startTime, endTime)

                  make_db_json(cmpct_height, receiveTime, stored_id, startTime.strftime("%Y-%m-%d %H:%M:%S.%f"))

                  print(db_json)

                  reset_value_block()

                  save_maria_anl_db()

                  db_json = {}

                     

            stored_id = stored_id + 1

         except Exception as ex:

            print("err : " + str(ex))

            reset_value()

            db_json = {}

 

# Save at MariaDB Analysis

def save_maria_anl_db():

   global db_json

   conn_anl = maria_analysis_connect(blockchain)

   cur_anl = conn_anl.cursor()

   cur_anl.execute("INSERT INTO BCmpctTime_PerHeight VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE GetblocktxnTime = ?, Gs_id = ?, BlocktxnTime = ?, Bs_id = ?, ReconstructedTIme = ?, Res_id = ?, CmpctTime = ?, _id = ?, Timestamp = ?", (int(db_json['Height']), db_json['getblocktxnTime'], int(db_json['gs_id']), db_json['blocktxnTime'], int(db_json['bs_id']), db_json['reconstructedTime'], int(db_json['res_id']), db_json['CmpctTime'], int(db_json['_id']), db_json['Timestamp'], db_json['getblocktxnTime'], int(db_json['gs_id']), db_json['blocktxnTime'], int(db_json['bs_id']), db_json['reconstructedTime'], int(db_json['res_id']), db_json['CmpctTime'], int(db_json['_id']), db_json['Timestamp']))

   db_close(cur_anl, conn_anl)

 

# 시간 형변환

def change_dateTime(date, time):

   dateTime = datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S.%f')

   return dateTime

 

# 시간 계산

def calculate_timeInterval(startTime, endTime):

   timeInterval = (endTime - startTime).total_seconds()

   return timeInterval

 

# json 파일로 DB에 넣을 정보 저장

def make_db_json_cmpctblock(cmpct_height, receiveTime, stored_id, getblocktxnTime, gs_id, blocktxnTime, bs_id, reconstructedTime, res_id, timestamp):

   global db_json

   db_json['Height'] = cmpct_height

   db_json['CmpctTime'] = receiveTime

   db_json['_id'] = stored_id

 

   db_json['getblocktxnTime'] = getblocktxnTime

   db_json['gs_id'] = gs_id

   db_json['blocktxnTime'] = blocktxnTime

   db_json['bs_id'] = bs_id

   db_json['reconstructedTime'] = reconstructedTime

   db_json['res_id'] = res_id

   db_json['Timestamp'] = timestamp

   

 

# json 파일로 DB에 넣을 정보 저장

def make_db_json(height, receiveTime, stored_id, timestamp):

   global db_json

   db_json['Height'] = height

   db_json['CmpctTime'] = receiveTime

   db_json['_id'] = stored_id


   db_json['getblocktxnTime'] = 0
   
   db_json['gs_id'] = 0
   
   db_json['blocktxnTime'] = 0
   
   db_json['bs_id'] = 0
   
   db_json['reconstructedTime'] = 0
   
   db_json['res_id'] = 0

   db_json['Timestamp'] = timestamp

 

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

 

def reset_value_block():

   global get_block_height

   global get_block_startTime

   get_block_startTime = False

   get_block_height = False

 

 

#=======================================본문========================================#

# Connect MariaDB Analysis AND Check The last Pos

blockchain = "Bitcoin"

conn_anl = maria_analysis_connect(blockchain)

cur_anl = conn_anl.cursor()

 

# Set Parameter

set_id = 0

cur_anl.execute("SELECT MAX(_id) FROM BCmpctTime_PerHeight")

row = cur_anl.fetchone()

set_id = row[0]

cur_anl.close()

 

if set_id is None or set_id == None:

    stored_id = 1

else:

    stored_id = int(set_id)

 

print(stored_id)

 

# Connect mongoDB

collection = "M0"

myclient = mongo_connect()

mydb = myclient[blockchain]

mycol = mydb[collection]

 

 

open_debug_log(mycol, stored_id)

 

myclient.close()
