#putText로 영상에 글자 표시하기
from ultralytics import YOLO
import cv2

#1.모델 로드
model=YOLO("yolo11n.pt")

#2.URL 설정
stream_url="http://210.99.70.120:1935/live/cctv009.stream/playlist.m3u8"
cap=cv2.VideoCapture(stream_url)
#3.실시간 프레임 처리
while cap.isOpened():
    success,frame=cap.read()
    if not success:
        print("프레임 또는 주소 확인")
        break
    #성공했을때
    #3-1.모델 추론
    results=model(frame, conf=0.2)#신뢰도를 0.2로
    #3-2.박스가 그려진 프레임 얻기
    annotated_frame=results[0].plot()

    #3-3.표시할 값 설정
    count= len(results[0].boxes)
    
    #탐지 개수에 따라 상태 색상 변경
    if count >=20:
        status,color="danger",(0,0,255)     #20개 이상: 빨강
    elif count>=15:
        status,color="warning",(0,165,255)  #15개 이상: 주황
    else:
        status,color="safe",(0,255,0)       #15개 미만: 초록
    print(f"마지막 탐지 개수: {count}, 상태: {status}")

    #3-4.탐지 객체 수 및 상태 화면에 표시
    cv2.putText(
        annotated_frame,    #텍스트 표시할 영상
        f"Detevted: {count},{status}",  #표시할 텍스트
        (10,30), #표시할 텍스트 위치 좌표
        cv2.FONT_HERSHEY_SIMPLEX,    #텍스트 폰트 스타일
        1,  #폰트 크기
        color,  #글자색
        2,  #글자두께
        cv2.LINE_AA #안티에일리어싱

    )
    #3-5.윈도우 창 출력
    cv2.imshow("CCTV_YOLO",annotated_frame) #창 이름, 탐지된 프레임 담긴 변수명    
    #3-6.q키를 눌러 종료
    if cv2.waitKey(1)& 0xFF == ord("q"):
        print("q키를 눌러서 종료됩니다.")
        break
#4.자원해제
cap.release()
cv2.destroyAllWindows()

