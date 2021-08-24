import numpy as np
from pandas import DataFrame
from pandas import read_csv
import csv



# csv 파일 읽어오기
csv_F = read_csv("\\\\210.125.29.157\\comnet\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정(코드, csv)\\Subnode_receivedCmpctTime\\210420 - 122개\\요청한 트랜잭션의 lockTime+size.csv")


lockTime = csv_F['lockTime']
size = csv_F['size']

# 평균, 중앙값, 표준편차, 최대, 최소
average = np.mean(size)
median = np.median(size)
standardDeviation = np.std(size)
max_value = np.max(size)
min_value = np.min(size)

print("avg = " + str(average))
print("median = " + str(median))
print("standardDeviation = " + str(standardDeviation))
print("max = " + str(max_value))
print("min = " + str(min_value))



lockTime_Num = {}

# 락타임 개수 구하기
for t in lockTime:
    if t in lockTime_Num :
        lockTime_Num[t] = lockTime_Num[t] + 1
    else :
        lockTime_Num[t] = 1


with open('\\\\210.125.29.157\\comnet\\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정(코드, csv)\\Subnode_receivedCmpctTime\\210420 - 122개\\reqeustTx_lockTime_Num.csv','w') as f:
    w = csv.writer(f)
    for k,v in lockTime_Num.items() :
        w.writerow([k,v])








