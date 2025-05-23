# export PYTHONIOENCODING=utf-8

import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import re
import json
import time


# terminal_input = json.loads(input())
terminal_input = input().split(',')
# print(terminal_input)

stopID = int(terminal_input[0])

# 초 단위; 곧 도착하는 노선의 남은 시간
arrives_soon_cut = int(terminal_input[1])

# request data
key = terminal_input[2]

queryParams = '?' + 'serviceKey=' + key + '&' + urlencode({'pageNo': '1', 'numOfRows': '50', 'stopid': stopID})

# API request
url = 'http://openapi.its.ulsan.kr/UlsanAPI/getBusArrivalInfo.xo' + queryParams

# 현재 정류소 도착 정보 저장하는 딕셔너리.
busstop_arrivalDataDict = {}
# 곧 도착하는 노선 번호 저장하는 리스트
busstop_routeArrivesSoon = []
# js json.parse 시 오름차순 정렬 -> 먼저 도착하는 노선 먼저 표시하도록 순서 보존하는 리스트
busstop_arrivalOrder = []

for i in range(5):
    try:
        request = urllib.request.urlopen(url)
        break
    except (HTTPError, URLError):
        # print(e.reason)

        # retry 5 times if failed
        time.sleep(5)
        if i == 4:
            busstop_arrivalDataDict["error"] = "error"
            busstop_arrivalDataDict["stopID"] = stopID
        else:
            continue


# 받은 정보 XML 파싱 준비
xmlData = request.read().decode('utf-8')

if 'SUCCESS' not in xmlData:
    # print("!ERROR: error in received data")
    busstop_arrivalDataDict["error"] = "error"
    busstop_arrivalDataDict["stopID"] = stopID
else:
    tree = ET.fromstring(xmlData)
    # print(tree.tag)
    for i in tree.iter('row'):
        # 도착정보 스트링 초기화
        busArrivalDataList = []
        routeNM = i.findtext('ROUTENM')
        routeNM = routeNM[:4]
        # routeNM_intonly_regexobj = re.match('[0-9]+', routeNM)
        # routeNM_intonly = int(routeNM_intonly_regexobj.group())
        # print(routeNM_intonly, end=": ")
        arrivalTime = int(i.findtext('ARRIVALTIME'))
        # 30분 이상 걸리는 노선은 표시하지 않음
        if arrivalTime > 1800:
            continue
        elif arrivalTime < arrives_soon_cut:
            busArrivalDataList.append('곧 도착')
            if routeNM not in busstop_routeArrivesSoon:
                busstop_routeArrivesSoon.append(routeNM)
        else:
            # print(str(int(arrivalTime / 60)) + '분', end=", ")
            busArrivalDataList.append(str(int(arrivalTime / 60)) + '분')

        prevStopCount = i.findtext('PREVSTOPCNT')
        # print(prevStopCount + '정거장 전', end='(')
        busArrivalDataList.append(prevStopCount + '전')
        presentStop = i.findtext('PRESENTSTOPNM')
        # print(presentStop + ')')
        busArrivalDataList.append('(' + presentStop + ')')

        if routeNM not in busstop_arrivalDataDict:
            busstop_arrivalDataDict[routeNM] = busArrivalDataList
            busstop_arrivalOrder.append(routeNM)
            # busstop_arrivalDataDict[routeNM] = busArrivalDataString


# 오름차순 정렬, key 값 기준
def sortDict(dictToSort):
    sortedDict = {}
    for i in sorted(busstop_arrivalDataDict):
        sortedDict[i] = dictToSort[i]

    return sortedDict


# busstop_arrivalDataDict = sortDict(busstop_arrivalDataDict)
if len(busstop_arrivalDataDict) < 1:
    busstop_arrivalDataDict["no_data"] = "no_data"
    busstop_arrivalDataDict["stopID"] = stopID
    print(json.dumps(busstop_arrivalDataDict, ensure_ascii=False))
else:
    busstop_arrivalDataDict["arrives_soon"] = busstop_routeArrivesSoon
    busstop_arrivalDataDict["stopID"] = stopID
    busstop_arrivalDataDict["arrival_Order"] = busstop_arrivalOrder
    print(json.dumps(busstop_arrivalDataDict, ensure_ascii=False))
