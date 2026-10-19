from ultralytics import solutions
import cv2

#1.비디오 경로 설정
cap=cv2.VideoCapture("https://cctvsec.ktict.co.kr/6570/slzNyfjZScqUil9yWzqaoUq8/R3+/mMGzREp1KdddCU9L4XmpTjAHyG/oEyUeNsY")
#2.라인 설정
line_points={
    "line1":[(288,265),(473,327)],
    "line2":[(268,250),(123,405)],
}
# 클릭된 좌표는(288, 265) 입니다.
# 클릭된 좌표는(473, 327) 입니다.
#3.모델 로드
#선마다 ObjectCounter를 하나씩 만듦 (ObjectCounter는 region을 하나만 받음)
counters={name: solutions.ObjectCounter(model="yolo11n.pt", region=pts)
          for name, pts in line_points.items()}
#4.프레임 처리
while cap.isOpened():
    success, frame=cap.read()
    if not success:
        print("프레임 확인해주세요")
        break
    #4-1.프레임 리사이즈
    re_frame=cv2.resize(frame,(640,480))
    #4-2.모델 추론
    for name, counter in counters.items():
        results=counter(re_frame)#마지막 선의 결과가 results에 남음
    #4-3.윈도우 창 띄우기
    cv2.imshow("IN/OUT COUNT",results.plot_im)
    #4-4.q키 눌러 종료
    if cv2.waitKey(1)&0xFF==ord('q'):
        print("q키를 눌러 종료")
        break
#5.자원 해제
cap.release()
cv2.destroyAllWindows()