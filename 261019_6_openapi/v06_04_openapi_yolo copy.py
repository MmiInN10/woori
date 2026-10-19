import urllib.request  #인터넷 주소로 자료 오청하는 도구
import json         #글자로 된 자료를 사전 모양으로 변환하는 도구
import pandas as pd #자료를 엑셀 같은 표로 다루는 도구
from ultralytics import YOLO
import cv2

#03번 함수 import해서 가져오기
from v06_03_openapi_yolo import cctv
input_url=cctv(50)

#9.프레임 설정
cctv_url=cctv(50)#50번째 CCTV 주소를 받아옴
cap=cv2.VideoCapture(cctv_url)

#10.모델 로드
model=YOLO("yolo11n.pt")

#11.프레임 처리
while cap.isOpened():
    success,frame=cap.read()
    if not success:
        print("프레임 확인해")
        break
    results=model(frame)
    annotated_frame=results[0].plot()
    
    #11-1. 윈토우 창 설정 및 띄우기
    cv2.namedWindow("OPENAPI",cv2.WINDOW_NORMAL)    #창 크기 조절
    cv2.imshow("OPENAPI",annotated_frame)
    
    #11-2. q키를 눌러서 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('q키를 눌러 종료')
        break
    
#12.자원 해제
cap.release()
cv2.destroyAllWindows()

#주석 1~8을 함수로 만들어라
    #매개변수: cctv_index
    #return:cctv_url
    