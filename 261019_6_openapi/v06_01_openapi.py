import urllib.request  #인터넷 주소로 자료 오청하는 도구
import json         #글자로 된 자료를 사전 모양으로 변환하는 도구
import pandas as pd #자료를 엑셀 같은 표로 다루는 도구

#1.인증 키
key=""
#과금 우려있는 api key는 코드 노출 깃허브 업로드 금지
#.env환경변수로 관리
#2.도로 유형(its=일반도로,ex=고속도로)->어느 도로 CCTV가져올 건지
road_type="its"

#3.관심 영역(경도, 위도 범위)
minX, maxX = 120.95, 127.02   # 동서(가로) 범위 → 한국 전체 가로
minY, maxY = 30.55, 37.69     # 남북(세로) 범위 → 한국 전체 세로
getType="json"      #응답 형식 : JSON(글자로 정리된 자료)

#4.API URL 조립
url_cctv = (
    f"https://openapi.its.go.kr:9443/cctvInfo"
    f"?apiKey={key}&type={road_type}&cctvType=1"
    f"&minX={minX}&maxX={maxX}"
    f"&minY={minY}&maxY={maxY}&getType={getType}"
)
#5.요청(만든 주소로 "자료 주세요")
response=urllib.request.urlopen(url_cctv)
# print(response)/
#<http.client.HTTPResponse object at 0x0000022E501740A0>

json_str=response.read().decode("utf-8")
# print(json_str)
#{"response":{"coordtype":1,"datacount":0}}

#6.bytes->str
json_dict=json.loads(json_str)
# print(json_dict)
#{'response': {'coordtype': 1, 'datacount': 0}}

#7.데이터 프레임 변환
cctv_play=pd.json_normalize(
    json_dict["response"]["data"], sep=''
)
print(cctv_play)
#8.CCTV URL 출력
test_url=cctv_play["cctvurl"][4]
print(f"선택된 CCTV URL : {test_url}")