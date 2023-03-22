## Master
: 압축 블록 시간 측정 및 블록 관련 데이터 수집, 이후 데이터베이스(MongoDB)에 저장

**파일이름**   
사용용도_사용방법_데이터

  * 사용용도
    - bcmon : bcmon 과제 코드
    - research : 연구


  * 사용방법
    - input : 데이터 수집


  * 데이터
    - receivedCmpctTime : 압축 블록 전달 시간
    - blockCreateTime : 블록 생성 시간
    - blocksize : 블록 크기
    - mempoolTxAndblockTx : 노드의 멤풀 내 트랜잭션과 블록의 트랜잭션 비교
    - mempoolData : 멤풀 정보
    - mempoolTx_compare6Node : 6개 노드의 멤풀 내 트랜잭션 비교
    - nTx : 블록의 트랜잭션 개수
    - rTxS+rTxT : 요청한 트랜잭션 사이즈와 트랜잭션을 요청했을때 걸린 시간
    - requestedTxnSize : 요청한 트랜잭션의 사이즈
    - usingCacheValidatingBlock : UpdateTip 로그에 찍힌 cache (UTXO)
