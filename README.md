## Bitcoin Received Cmpct BlockTime
: 비트코인 압축 블록 전달 시간 측정 및 분석

현재 비트코인 블록 전달 방식으로는 기존에 존재하던 Legacy Protocol과 전달 시간 단축을 위해 개발된 Compact Block Relay 프로토콜이 있음.   
Legacy Protocol은 블록을 전달할 때 블록 헤더와 함께 블록에 포함된 전체 트랜잭션을 전달.   
Compact Block Relay 방식은 블록에 포함된 트랜잭션 중에서 수신하는 노드의 메모리 풀에 이미 저장되어 있는 트랜잭션은 전달하지 않음으로써 블록 전달을 효율적으로 수행하는 방식.  

Compact Block Relay 방식에 대하여 실제 비트코인 네트워크 내에 구성된 노드를 사용해 전달 시간을 측정. 또한, 전달 시간이 지연된 원인을 분석하여 블록 전달 시간을 단축하기 위한 연구에 기초 데이터를 제공함(비트코인의 블록은 노드를 거쳐서 전체 네트워크로 전파되기 때문에 전체 네트워크로 블록이 전파되는 시간은 노드 간의 전달 시간에 영향을 받으며, 블록 전달 시간을 단축하면 전체 노드에 전파되는 블록 전파 시간을 단축할 수 있고 비트코인 성능이 향상).   

해당 Repository는 압축 블록 전달 시간을 측정하고 분석하는 코드 저장소임.


## How to Use
: 각 Branch로 이동 후 README.md 파일 참고


* * *

> **관련 논문**   
* 비트코인 네트워크의 압축 블록 전달 지연 개선 / 김애리[저] - 계명대학교 석사 학위 논문
* IJNM   
* 김애리, 주홍택, "비트코인 노드의 압축 블록 전달 지연 원인 분석", 통신망운용관리 학술대회(KNOM Conf. 2021), pp. 69-79, Apr. 2021.
* Aeri Kim, Jungyeon Kim, Meryam Essaid, Sejin Park, Hongtaek Ju, "Analysis of Compact Block Propagation Delay in Bitcoin Network", Asia-Pacific Network Operations and Management Symposium (APNOMS 2021), Sep. 2021.
* 김애리, 주홍택,"비트코인 네트워크에서 압축 블록 전달 방식의 전송 지연 분석", 한국통신학회논문지, Vol. 47, No. 6, pp. 826-835, Jun. 2022 (KCI)
