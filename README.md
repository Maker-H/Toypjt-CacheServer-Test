## 캐시 서버가 필요한 이유
- 클라이언트-웹서버-웹어플리케이션서버-데이터베이스 구조에서 가장 큰 병목 현상은 데이터베이스에서 발생
- 웹애플리케이션 서버는 데이터베이스 서버에 쿼리를 보내고 데이터를 검색, 삽입, 수정하기 위해 데이터베이스와 상호작용하는데 데이터베이스를 읽을때 그 값을 찾아 들어가야하기 때문에 부하가 많이 걸림
- 데이터를 캐시 서버에 저장하고 바로 읽을 수 있다면 데이터베이스 안에서 데이터를 검색하는 시간이 많이 절약될 수 있습니다
