# 결과
- locust로 부하 테스트 시행 
<redis를 사용하지 않았을 때>
![image](https://github.com/Maker-H/Toypjt-CacheServer-Test/assets/83294376/e67477f7-f40c-4ff6-8eac-c42833fee8ab)

Response time percentiles (approximated)
Type     Name      50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------|------|------|------|------|------|------|------|------|------|------|------|------|
GET       /test     110   200    280     330    470    600    840    970   1500   1800   1800   5843
--------|--------|------|------|------|------|------|------|------|------|------|------|------|------|




<redis를 사용했을 때>
![image](https://github.com/Maker-H/Toypjt-CacheServer-Test/assets/83294376/9b3574d9-b482-44a7-a195-3d8550767978)


Response time percentiles (approximated)
|Type     Name      50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs|
|--------|--------|--------|------|------|------|------|------|------|------|------|------|------|------|
|GET      /redis     27      34      39     43     55     67     88     110    170   190    190     7578|
|--------|--------|--------|------|------|------|------|------|------|------|------|------|------|------|



# 추가로 더 해볼 것
- TTL에 의존하는 것이 아니라 데이터 변경시 기존 캐시 만료 시키기 [link](https://jupiny.com/2018/02/27/caching-using-redis-on-django/)

# 캐시

## 캐시 서버가 필요한 이유
- 클라이언트-웹서버-웹어플리케이션서버-데이터베이스 구조에서 가장 큰 병목 현상은 데이터베이스에서 발생
- 웹애플리케이션 서버는 데이터베이스 서버에 쿼리를 보내고 데이터를 검색, 삽입, 수정하기 위해 데이터베이스와 상호작용하는데 데이터베이스를 읽을때 그 값을 찾아 들어가야하기 때문에 부하가 많이 걸림
- 데이터를 캐시 서버에 저장하고 바로 읽을 수 있다면 데이터베이스 안에서 데이터를 검색하는 시간이 많이 절약될 수 있습니다

## 리버스 프록시 캐싱
- 웹서버로 유입되는 HTTP 트래픽을 캐슁 시스템이 저장하고 있다가 동일 요청이 들어왔을때 캐슁 시스템이 이 데이터를 돌려줌으로써 빠른 응답을 제공하는 것


## 웹페이지 캐싱
- 웹페이지 캐싱(페이지 캐싱)은 페이지 전체를 캐슁하는 방법이다
- 한 번 캐쉬가 만들어지면 동일한 url로 진입하는 요청은 캐쉬 파일의 내용을 읽어서 사용하고 처리가 종료되기에 시간이 절약된다

## 부분 캐싱
- 웹페이지 캐싱은 모든 페이지를 캐쉬하기 때문에 데이터의 갱신이 자주 일어나지 않고 사용자 인증 기능이 없는 페이지를 캐싱하는데 적합하다
- 일부 데이터만을 저장할 때는 다른 방법을 사용해야 하고 그때 사용하는 것이 부분 캐싱이다
- 페이지 구성 요소 데이터의 일부만을 캐싱하고 싶으면 주로 데이터베이스에 데이터를 저장했다가 동일 요청이 있을때 저장된 데이터를 사용함으로써 데이터베이스의 부담을 경감시키고 반응 속도를 높일 수 있다

### 부분 캐싱의 문제점
- 데이터가 변했는데 캐시가 살아있을 수 있다는 문제가 있다 TTL을 사용해서 일정 시간이 지나면 캐시를 만료시킬 수 있지만 그 전에 데이터가 업데이트 되었을때도 예전의 데이터가 계속 보인다는 문제점이 있다
- 데이터의 업데이트가 이루어졌을때 해당 캐쉬를 명시적으로 무효화 시키는 방법으로 해결할 수 있다


# Redis

## Redis란?
- 고성능 key-value 저장소로서 리스트, 해시, 셋, 정렬된 셋 등 여러 자료구조를 지원하는 NoSQL
- 메모리에 상주하며 RMDBMS의 캐시 솔루션으로 사용됨
- RMDBMS의 read 부하를 줄이는데 사용됨
- C언어로 작성되었기에 가상 머신 위에서 인터프리터된 언어로 가동되는 경우에 발생하는 가비지 컬렉션 동작에 따른 성능 문제가 발생하지 않음


## Redis 안정성
- snapshot: 특정 시점의 데이터를 디스크에 옮겨담는 방식
- AOF: Redis의 모든 write/update 연산을 log 파일에 기록하는 방식, 서버가 재시작될 때 write/update를 순차적으로 재실행해서 데이터를 복구함
- 주기적으로 snapshot으로 백업한 이후 snapshot까지의 저장을 AOF 방식으로 수행하는 것을 권장

## 샤딩
- 데이터를 여러 개의 작은 조각인 샤드로 분할하여 분산 시스템에 분산시키는 작업 
- 샤딩을 통해 데이터를 여러 대의 레디스 서버에 분산 저장할 수 있기에 처리 능력이 증대됨

## 토폴로지 
- 레디스 클러스터의 구성 방식을 나타내는 것으로, 노드 간의 관계와 연결 형태를 나타냄, 주로 마스터-슬레이브 방식

### 마스터 노드의 Redis에서의 작업 흐름
1. 클라이언트 요청 수신: 마스터 노드는 데이터 생성, 수정, 삭제와 같은 쓰기 작업을 클라이언트로부터 요청받음
2. 데이터 처리: 마스터 노드는 해당 작업을 처리함
3. 데이터 변경 사항 복제: 동일한 데이터 변경 작업을 슬레이브 노드들에게 비동기적으로 복제함, 슬레이브 노드는 마스터 노드의 변경사항을 실시간으로 수신하여 자신도 마스터 노드와 같은 정보를 담음


### 슬레이브 노드의 Redis에서의 작업 흐름
1. 클라이언트 요청 수신: 슬레이브 노드는 클라이언트로부터 읽기 작업 요청을 받음, 슬레이브 노드가 자체적으로 처리
2. 데이터 검색: 슬레이브 노드는 클라이언트의 요청애 대해 자신의 로컬 데이터(Redis)를 검색, 캐시 서버로 작동

