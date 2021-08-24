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
csv = read_csv("\\\\210.125.29.157\\comnet\\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정\\Subnode_receivedCmpctTime\\compare_4\\sejong.csv")


fig_name = '\\\\210.125.29.157\\comnet\\Computer Network Lab\\멤버\\재학생\\김애리\\연구\\비트코인 전달 시간 측정\\Subnode_receivedCmpctTime\\compare_4\\sejong.png'


startIndex = 0
isStart = False
endIndex = 0
tmpIndex = 0
for data_row in csv['_id'] :
    if int(data_row) > 656000 and isStart is False:
        startIndex = tmpIndex
        isStart = True
    if int(data_row) > 656500 :
        endIndex = tmpIndex - 1
        break
    tmpIndex = tmpIndex + 1

# 축 데이터
xtext = list(csv.loc[startIndex:endIndex]['_id'])    # x축에 넣을 데이터
pyplot.ylim(0, 100) # y 축 범위 지정
print(len(csv.loc[startIndex:endIndex].index))

# 그래프 그리기
csv.loc[startIndex:endIndex]['time_lack'].plot(color='#ff0000')
pyplot.grid()
pyplot.legend()
pyplot.xlabel("블록 높이")
pyplot.ylabel("전달 시간 (초)")
pyplot.xticks(csv.loc[startIndex:endIndex].index, xtext, rotation=90, fontsize=12) # x 축
pyplot.locator_params(axis='x', nbins=100) # x축의 개수 줄여주기
pyplot.subplots_adjust(left = 0.05, bottom = 0.15, right = 0.97, top = 0.97, hspace = 0.2, wspace = 0.2) # 그래프 창에 맞춰서 그리기
pyplot.savefig(fig_name)
pyplot.show()

