from ultralytics import solutions
import cv2

#1.비디오 경로 설치
stream_url="https://cctvsec.ktict.co.kr/1872/LGwOYzKD3KK7iJTdqaj9mxFiTEGeIuIbZmU/Lgu7L1pPD2n09JsTUjm6t+wGVGmt"
cap=cv2.VideoCapture(stream_url)

#2.이메일 정보 설정
from_email="kimmin6303@gmail.com"
password=""
#구글 앱 인증에서 인증받고 받은 비밀번호 붙여넣기
to_email="kimmin6303@gmail.com"
#3.모델 로드(알림 객체 생성)
google_alarm=solutions.SecurityAlarm(
    model="yolo11n.pt",
    show=False,
    classes=[2],#차량만 탐지
    records=3   #3개 이상 탐지되면 매일 1회 전송
)
#4.SMTP 서버 인증
google_alarm.authenticate(from_email, password, to_email)

#5.비디오 프레임 처리
while cap.isOpened():
    success, frame=cap.read()
    if not success:
        print("프레임 확인 ")
        break
    #5-1.모델 추론
    results=google_alarm(frame)
    #5-2.윈도우 창 표시
    cv2.imshow("SECFURITY_ALARM", results.plot_im)
    
    #5-3.q키를 눌러서 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("q키를 눌러 종료")
        break
    
#6.자원 해제
cap.release()
cv2.destroyAllWindows()

#과제. 기본 알림 문구를 수정하기->"현재 경고이므로 주의해주세요."
