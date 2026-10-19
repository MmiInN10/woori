from ultralytics import YOLO
import time
import cv2
#1.비디오 경로 설정
cap=cv2.VideoCapture("261016_4_yolo_advan/heatmap_video.mp4")
#2.모델 선택
model=YOLO("yolo11n.pt")

#3.프레임 처리
while cap.isOpened():
    success,frame=cap.read()
    if not success:
        print("프레임 확인해주세요")
        break
    #3-5:추론 시간 측정
    start_time=time.perf_counter()  #추론 시작 시간
    #3-2모델 추론
    results=model(frame,verbose=False,device="cpu")#터미널에 로그 출력X
    #3-3.추론 종료 시간 측정
    end_time=time.perf_counter()    #추론 종료 시간
    #3-4.FPS 계산
    if_time=end_time-start_time
    fps=1/if_time
    #3-5.결과 시각화
    annotated_frame=results[0].plot()
    #3-6.FPS표시
    cv2.putText(
        annotated_frame,
        f"{fps:.1f} FPS",
        (10,30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,  #폰트 크기(scale)
        (0,255,0),  #폰트 색상
        2   #폰트 굵기(thickness)
    )
    #3-7.윈도우 창 띄우기
    cv2.imshow("YOLO_FPS",annotated_frame)
    #3-8.q키눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("q키를 눌러 종료")    
        break
#4.자원 해제
cap.release()
cv2.destroyAllWindows()