import json
import re
import time
import sys
import mariadb
import pymongo
from pymongo import MongoClient
from datetime import date, datetime

#=======================================변수========================================#

# 정규식
pattern_startTime = re.compile(
    r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\s(received:\scmpctblock\s\(\d+\sbytes\)\speer\=\d+)")
pattern_getHash = re.compile(
    r"Initialized\sPartiallyDownloadedBlock\sfor\sblock\s(?P<hash>\w+)\s(using\sa\scmpctblock\sof\ssize\s\d+)")
pattern_getblocktxn = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\ssending\sgetblocktxn\s\(\d+\sbytes\)\speer=\d+")
pattern_blocktxn = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sreceived[:]\sblocktxn\s\((?P<size>\d+)\sbytes\)\speer=\d+")
pattern_endTime = re.compile(r"(?P<date>\d+[-]\d+[-]\d+)T(?P<time>\d+[:]\d+[:]\d+[.]\d+)Z\sSuccessfully\sreconstructed\sblock\s(?P<hash>\w+)\swith\s\d+\stxn\sprefilled\,\s\d+\stxn\sfrom\smempool\s\(incl\sat\sleast\s\d+\sfrom\sextra\spool\)\sand\s(?P<rtx>\d+)\stxn\srequested")
pattern_getHeight = re.compile(r"UpdateTip[:]\snew\sbest\=(?P<hash>\w+)\sheight[=](?P<height>\d+)\sversion\=\w+\slog2[_]work\=\d+[.]\d+\stx\=\d+\sdate\=\'\d+[-]\d+[-]\d+T\d+[:]\d+[:]\d+Z\'\sprogress\=\d+[.]\d+\scache\=\d+[.]\d+MiB\(\d+txo\)")

# 값을 차례대로 얻기 위한 boolean
get_startTime = False
get_height = False
get_hash = False
get_getblocktxn = False


# 컬렉션에 저장할 때 사용할 json 배열
db_json = {}


#=======================================함수========================================#
def connect_monogoDB():
    myclient = pymongo.MongoClient("mongodb://210.125.29.227:27017/")
    mydb = myclient['Bitcoin']
    collection = mydb["M0"]

    return collection



# maria db connect
def connectMariaDB():
    global conn_db
    global cur


    # connect MariaDB
    conn_db = mariadb.connect(
            user="root",
            password="Cn*dntwk",
            host="210.125.29.227",
			#host="169.254.229.88",
			#host="169.254.31.40",
            port=3306,
            database="Bitcoin"
            )

    # create cursor
    cur = conn_db.cursor()

def connectRawMariaDB():
	# connect MariaDB
    conn_db = mariadb.connect(
			user="root",
			password="Cn*dntwk",
			host="210.125.29.227",
			port=3406,
			database="Bitcoin"
			)
    cur = conn_db.cursor()
    return conn_db, cur

# debug log read and write
def collectData(collection):
	global get_startTime
	global get_height
	global get_hash
	global get_getblocktxn
	global db_json

	stored_id = 3528400#load_pos()
	conn_raw, cur_raw = connectRawMariaDB()

	
	# 라인 읽기 및 비교와 데이터 추출
	while True:
		mydoc = collection.find_one({"_id": stored_id}, {"_id": 0, "log": 1})
		
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

			if pattern_getHash.search(line) and not get_hash:
				find_line = pattern_getHash.search(line)
				cmpct_hash = find_line.group('hash')
				get_hash = True

			if pattern_getblocktxn.search(line) and get_hash :
				get_getblocktxn = True

			if pattern_blocktxn.search(line) and get_getblocktxn :
				find_line = pattern_blocktxn.search(line)
				gtxS = int(find_line.group('size')) - 33

			if pattern_endTime.search(line) and get_hash :
				find_line = pattern_endTime.search(line)
				if find_line.group('hash') == cmpct_hash :
					endTime = change_dateTime(find_line.group(
                         'date'), find_line.group('time'))
					gtxN = int(find_line.group('rtx'))

			"""
			if pattern_KAR_received_blockTxn.search(line) and get_getblocktxn :
				find_line = pattern_KAR_received_blockTxn.search(line)
				if find_line.group('blockHash') == cmpct_hash :		# 요청한 트랜잭션 리스트를 만듦
						requestTxn.append(find_line.group('hash'))
			"""
						
				
			if pattern_getHeight.search(line) and get_hash:
				find_line = pattern_getHeight.search(line)
				if cmpct_hash == find_line.group('hash'):
					cmpct_height = int(find_line.group('height'))
					if get_getblocktxn is False :
						gtxN = 0
						gtxS = 0
					receiveTime = calculate_timeInterval(startTime, endTime)
					timestamp = loadBlockTimestamp(cur_raw, cmpct_height)
					make_db_json(cmpct_height, gtxN, gtxS, stored_id, receiveTime, timestamp)
					excuteSQL(db_json)
					reset_value()
					#save_maria_anl_db()
					db_json = {}
								
			stored_id = stored_id + 1
		except Exception as ex:
			print("err : " + str(ex))
			reset_value()
			db_json = {}
			
	f.close()
	conn_raw.close()


def excuteSQL(info):
	global cur
	sql = "INSERT INTO BGetblocktxnInfo_PerHeight VALUES("+ str(info["Height"]) + "," + str(info["GetblocktxnNum"]) + "," + str(info["GetblocktxnSize"]) + "," + str(info["_id"]) + "," + str(info["CmpctTime"]) + ",'" + info["TimeStamp"] +"')"
	cur.execute(sql)
	dbSave()


def dbSave():
	global conn_db

	conn_db.commit()

def dbClose():
    global conn_db
    # close
    conn_db.close()

def loadBlockTimestamp(cur_raw,height):
    cur_raw.execute("SELECT Height, Blocktime From BBlock WHERE "+str(height)+"=Height ORDER BY Height ASC")
    getblock = cur_raw.fetchone()
    date_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(getblock[1])))

    return date_time


# 시간 형변환

def change_dateTime(date, time):
   dateTime = datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S.%f')
   return dateTime


# 시간 계산
def calculate_timeInterval(startTime, endTime):
   timeInterval = (endTime - startTime).total_seconds()
   return timeInterval


# json 파일로 DB에 넣을 정보 저장
def make_db_json(height, gtxN, gtxS, stored_id, time, timestamp):
	global db_json
	db_json['Height'] = height
	db_json['GetblocktxnNum'] = gtxN
	db_json['GetblocktxnSize'] = gtxS
	db_json['_id'] = stored_id
	db_json['CmpctTime'] = time
	db_json['TimeStamp'] = timestamp

# 다시 false로 변환, 값 초기화
def reset_value():
	global get_startTime
	global get_height
	global get_hash
	global get_getblocktxn
	
	get_startTime = False
	get_height = False
	get_hash = False
	get_getblocktxn = False

# 마리아 db에서 _id 불러오기
def load_pos():
	global cur
	# Set Parameter
	set_id = 0
	cur.execute("SELECT MAX(_id) FROM BGetblocktxnInfo_PerHeight")
	row = cur.fetchone()
	set_id = row[0]

	if set_id is None or set_id == None:
		stored_id = 1
	else:
		stored_id = int(set_id)

	return stored_id




#=======================================본문========================================#
# Connect MariaDB Analysis AND Check The last Pos

connectMariaDB()
collectData(connect_monogoDB())
dbSave()
dbClose()

