#%%
import numpy
from pandas import DataFrame
from pandas import read_csv
from matplotlib import pyplot
import datetime


# 폰트 지정
pyplot.rcParams["font.family"] = 'Malgun Gothic'
pyplot.rcParams["font.size"] = 16
pyplot.rcParams["figure.figsize"] = (20, 10)

# csv 파일 읽어오기
csv = read_csv("\\\\210.125.29.157\\comnet\\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정\\Subnode_receivedCmpctTime\\201110-656265\\201110_Subnode_receivedCmpctTime(654000-656000)_endTime.csv")

# 날짜 자르기 (원하는 날짜로 자르기) csv.loc[startIndex:endIndex] <-- 잘라진 csv

#==================여기 날짜만 수정하면 됨======================#

day = 8
startDate = datetime.datetime(2020, 11, day, 00, 00)
endDate = datetime.datetime(2020, 11, day + 1, 00, 00)
fig_name = '\\\\210.125.29.157\\comnet\\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정\\Subnode_receivedCmpctTime\\201110-656265\\그래프\\11-' + str(day) +'.png'
#=============================================================#

startIndex = 0
isStart = False
endIndex = 0
tmpIndex = 0
for date_row in csv['endTime'] :
    date_result = datetime.datetime.strptime("2020-" + date_row, "%Y-%m-%d %H:%M")
    if date_result >= startDate and isStart is False :
        startIndex = tmpIndex
        isStart = True
    if date_result > endDate:
        endIndex = tmpIndex - 1
        break
    tmpIndex = tmpIndex + 1
    if tmpIndex == len(csv.index):
        endIndex = tmpIndex



# 축 데이터
xtext = list(csv.loc[startIndex:endIndex]['endTime'])    # x축에 넣을 데이터
pyplot.ylim(0, 6) # y 축 범위 지정

# 그래프 그리기
csv.loc[startIndex:endIndex]['receiveTime_result'].plot(color='#ff0000')
pyplot.grid()
pyplot.legend()
pyplot.xlabel("날짜(MM-DD HH:mm)")
pyplot.ylabel("전달 시간 (초)")
pyplot.xticks(csv.loc[startIndex:endIndex].index, xtext, rotation=90, fontsize=12) # x 축
pyplot.locator_params(axis='x', nbins=len(csv.loc[startIndex:endIndex].index)/2) # x축의 개수 줄여주기
pyplot.subplots_adjust(left = 0.05, bottom = 0.15, right = 0.97, top = 0.97, hspace = 0.2, wspace = 0.2) # 그래프 창에 맞춰서 그리기
pyplot.savefig(fig_name)
pyplot.show()


