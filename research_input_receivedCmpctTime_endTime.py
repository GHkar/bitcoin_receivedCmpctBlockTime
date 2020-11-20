import pymongo
from pymongo import MongoClient
import json
import re
import datetime

#=======================================변수========================================#

 # 컬렉션에 저장할 때 사용할 json 배열
db_json = {}

#=======================================함수========================================#

# 몽고 db에 연결
def connect_monogoDB(collection_name):
    myclient = pymongo.MongoClient("mongodb://210.125.31.240:27017/")
    mydb = myclient['bitcoin']
    collection = mydb[collection_name]
    
    return collection

# 끝나는 시간 얻어서 다시 몽고 디비에 저장하기
def save_endTime():
    count = 0
    origin_collection_name = "SubNode_cmpctblock_received_time_per_height"
    origin_collection = connect_monogoDB(origin_collection_name)
    new_collection_name = "SubNode_cmpctblock_received_time_per_endTime"
    new_collection = connect_monogoDB(new_collection_name)
    
    take_data = origin_collection.find({},{"endTime":1, "receiveTime_result":1})
    
    for time in take_data:
        make_db_json(time['_id'], time['endTime'].strftime('%m-%d %H:%M'), time['receiveTime_result'])
        save_mongo_db(new_collection)
        count = count + 1
    
    print_result(count)

# 몽고 db에 저장
def save_mongo_db(collection):
    global db_json

    collection.insert_one(db_json)


# json 파일로 DB에 넣을 정보 저장
def make_db_json(height, endTime, receiveTime):
    global db_json

    db_json['_id'] = height
    db_json['endTime'] = endTime
    db_json['receiveTime_result'] = receiveTime



# 결과를 출력
def print_result(count):
    if count == 0:
        print("모든 데이터가 DB에 입력 완료된 상태입니다.")
    else :
        print("총 " + str(count) + "개를 DB에 저장하였습니다.")

#=======================================본문========================================#


save_endTime()

