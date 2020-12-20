# MMM-UlsanBus
MM2 module displays ulsan bus information.

![Alt text](/ulsanBus.png)         

https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15052669
울산광역시 BIS 정보 API 활용신청 후 운영계정 등록하신 뒤 인증키를
ulsan_busArrivalInfo.py 의 22번째 줄 key 변수에 넣고 사용하시면 됩니다.

## Embedding MMM-UlsanBus
``` JS
modules: [
  {
    module: "ulsanBus",
    position: "top_center",
    config: {
      busstop: {
        '법원(->공업탑R)': [193040605, 240],
        '법원(->무거삼거리)': [193040606, 240],
        '옥동주민센터(->옥동초)': [193040609, 240],
        '옥동주민센터(->법원)': [193040608, 240],
        '대륙현대2차아파트(->)': [193012613, 240],
        '대륙현대2차아파트(<-)': [193012614, 240],
      },
      updateInterval: 30000,
      busStopUpdateInterval: 10000,
      maxDisplayRoute: 8,
      maxDisplayBusStops: 2,
    }
  },
]
```
   


**busstop:** 안에 들어가는 딕셔너리 객체들은 **'정류장 이름': [정류장 번호, 곧 도착 표시 시간(초 단위)]**   
**정류장 번호**는 카카오맵 정류장 검색 시 나오는 번호 앞에 **1930**을 붙이면 대충 잘 동작하지만,   
울산광역시 BIS 정보 API의 **버스정류장정보 조회** 오퍼레이션을 이용하시면 보다 확실한 정보를 얻을 수 있습니다.
