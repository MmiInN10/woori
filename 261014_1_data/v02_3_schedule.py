import cv2 #카메라를 다루는 도구
import os #폴더를 만드는 도구
from datetime import datetime #지금 시간을 알려주는 도구
import schedule

#사진 캡쳐 간격 설정
interval_time=5

#위 코드를 함수로 만들어주세요
def capture_image():
    #[1단계]사진 저장할 폴더 준비
    save_dir="./captured_images" #./는 현재경로. 폴더명
    os.makedirs(save_dir, exist_ok=True)#저장할 경로, 폴더가 없으면 자동으로 만듬
    cap=cv2.VideoCapture(0)
    success, frame= cap.read() #success=True면 연결 성공,frame=찍힌 이미지
    if success:
        #사진 파일명 : 찍은 시간을 쓰면 여러 장을 찍어도 이름이 겹치지 않는다.. 언제 찍었는지 알 수 있다.
        timestamp=datetime.now().strftime("%Y%m_%H%M%S") 
        file_path=os.path.join(save_dir, f"result_{timestamp}.jpg")
        
        # 파일로 저장
        cv2.imwrite(file_path, frame)
        print(f"사진이 저장됐습니다.{file_path}")#잘 저장 됐는지 확인 메시지
    else:
        print("카메라 읽기 실패!!")

    #[4단계] 카메라 끕니다
    cap.release()

#스케쥴러 설정
schedule.every(interval_time).seconds.do(capture_image) #5초 간격으로 실행

#스케줄러 실행
while True:
    schedule.run_pending() #예약된 작업 실행