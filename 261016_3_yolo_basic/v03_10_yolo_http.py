from ultralytics import YOLO
import cv2

#1.모델 로드
model=YOLO("yolo11n.pt")

#2.cctv스트림 주소
stream_url="https://cctvsec.ktict.co.kr/6568/VALd7fN0yXqIzLwgqYAnHJ2MbTlO5zuCXc4kf+TdrzHK7qmvuX7N8INoLJzceALG"
cap=cv2.VideoCapture(stream_url)
#3.실시간프레임처리
while cap.isOpened(): #스트림이 열려있는 동안 반복
    success, frame=cap.read() #프레임과 성공여부 받기
    if not success:     #프레임을 받지 못했을때
        print("CCTV URL 또는 웹캠 확인해주세요.")
        break
    #t스트림 잘 읽어왔을때 처리
    #3-1.모델추론
    results=model(frame, conf=0.5)
    
    #3-2.탐지결과가 그려진 프레임 열기
    annotated_frame=results[0].plot()
    
    #3-3, 윈도우 창 그리기
    cv2.imshow("CCTV_YOLO", annotated_frame) #윈도우 창 이름, 탐지된 주소?
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("q키를 눌러서 종료")
        break
    
#4.자원해제
cap.release()
cv2.destroyAllWindows()