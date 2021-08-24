#%%
import numpy
from pandas import DataFrame
from pandas import read_csv
from matplotlib import pyplot

# 폰트 지정
pyplot.rcParams["font.family"] = 'Malgun Gothic'
pyplot.rcParams["font.size"] = 16
pyplot.rcParams["figure.figsize"] = (20, 10)

# csv 파일 읽어오기
csv = read_csv("../SubNode_receivedCmpctTime/201110-656265/201201_Subnode_receivedCmpctTime(654000-656000)_nTx.csv")

# 축 데이터
xtext = list(csv['_id'])    # x축에 넣을 데이터
xpos = numpy.arange(len(csv.index))

# 그래프 그리기
csv['ntx'].plot(color='#ff0000')
pyplot.grid()
pyplot.legend()
pyplot.xlabel("블록 높이")
pyplot.ylabel("nTx (블록의 트랜잭션 수)")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
pyplot.xticks(xpos, xtext, rotation=90, fontsize=12) # x 축
pyplot.locator_params(axis='x', nbins=100) # x축의 개수 줄여주기
pyplot.subplots_adjust(left = 0.05, bottom = 0.14, right = 0.97, top = 0.97, hspace = 0.2, wspace = 0.2)
pyplot.show()
