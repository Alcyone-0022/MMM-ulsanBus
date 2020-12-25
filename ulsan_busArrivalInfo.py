# export PYTHONIOENCODING=utf-8

import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import re
import json


# terminal_input = json.loads(input())
terminal_input = input().split(',')
# print(terminal_input)

stopID = int(terminal_input[0])

# 초 단위; 곧 도착하는 노선의 남은 시간
# arrives_soon_cut = 240
arrives_soon_cut = int(terminal_input[1])

# request data
# key = "TRekJec4iz%2BlT5wZwy56C3AxHC3YaM35svqI7HHTMx0PM3K%2BsuVZbVnRN8BAv%2BTgA6eAAXeT5m865H%2BvKW%2BecA%3D%3D"
key = terminal_input[2]

# # 대륙2차 193012613 법원(공업탑R방면) 193040605
# stopID = 193040605
queryParams = '?' + 'serviceKey=' + key + '&' + urlencode({'pageNo': '1', 'numOfRows': '50', 'stopid': stopID})

# API request
url = 'http://openapi.its.ulsan.kr/UlsanAPI/getBusArrivalInfo.xo' + queryParams

# 현재 정류소 도착 정보 저장하는 딕셔너리.
busstop_arrivalDataDict = {}
# 곧 도착하는 노선 번호 저장하는 리스트
busstop_routeArrivesSoon = []
# js json.parse 시 오름차순 정렬 -> 먼저 도착하는 노선 먼저 표시하도록 순서 보존하는 리스트
busstop_arrivalOrder = []

while True:
    try:
        request = urllib.request.urlopen(url)
        break
    except (HTTPError, URLError):
        # print(e.reason)
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
        # print("row")
        # 도착정보 스트링 초기화
        busArrivalDataList = []

        routeNM = i.findtext('ROUTENM')
        routeNM_intonly_regexobj = re.match('[0-9]+', routeNM)
        routeNM_intonly = int(routeNM_intonly_regexobj.group())
        # print(routeNM_intonly, end=": ")
        arrivalTime = int(i.findtext('ARRIVALTIME'))
        if arrivalTime < arrives_soon_cut:
            # print('곧 도착', end=', ')
            busArrivalDataList.append('곧 도착')
            busstop_routeArrivesSoon.append(routeNM_intonly)
        else:
            # print(str(int(arrivalTime / 60)) + '분', end=", ")
            busArrivalDataList.append(str(int(arrivalTime / 60)) + '분')
        prevStopCount = i.findtext('PREVSTOPCNT')
        # print(prevStopCount + '정거장 전', end='(')
        busArrivalDataList.append(prevStopCount + '전')
        presentStop = i.findtext('PRESENTSTOPNM')
        # print(presentStop + ')')
        busArrivalDataList.append('(' + presentStop + ')')

        busstop_arrivalDataDict[routeNM_intonly] = busArrivalDataList
        busstop_arrivalOrder.append(routeNM_intonly)
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
    print(json.dumps(busstop_arrivalDataDict, ensure_ascii = False))
else:
    busstop_arrivalDataDict["arrives_soon"] = busstop_routeArrivesSoon
    busstop_arrivalDataDict["stopID"] = stopID
    busstop_arrivalDataDict["arrival_Order"] = busstop_arrivalOrder
    print(json.dumps(busstop_arrivalDataDict, ensure_ascii = False))
