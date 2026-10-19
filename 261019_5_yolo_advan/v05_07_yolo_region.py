from ultralytics import solutions
import cv2
#1.비디오 경로 설정
cap=cv2.VideoCapture("https://cctvsec.ktict.co.kr/6570/slzNyfjZScqUil9yWzqaoUq8/R3+/mMGzREp1KdddCU9L4XmpTjAHyG/oEyUeNsY")
#2.영역 좌표 설정(dict 형식 - 키로 영역 구분)
region_points={
    "region1":[{131,77},{120,413},{594,410},{531,84}],
    "region2":[{414 ,58},{341,181},{482,195},{454,59}] 
}
# 클릭된 좌표는(131, 77) 입니다.
# 클릭된 좌표는(120, 413) 입니다.
# 클릭된 좌표는(594, 410) 입니다.
# 클릭된 좌표는(531, 84) 입니다.

# 클릭된 좌표는(414, 58) 입니다.
# 클릭된 좌표는(341, 181) 입니다.
# 클릭된 좌표는(328, 283) 입니다.
# 클릭된 좌표는(463, 310) 입니다.
# 클릭된 좌표는(482, 195) 입니다.
# 클릭된 좌표는(454, 59) 입니다.
#3.모델 로드
yolo_region=solutions.RegionCounter(
    model="yolo11n.pt",
    show=False,
    region=region_points
)
#4.프레임 처리
while cap.isOpened():
    success,frame=cap.read()
    if not success:
        print("프레임 확인해라")
        break
    #4-1.프레임 크기 조정(좌표계 통일)
    #해상도 동일하게 받도록
    re_frame=cv2.resize(frame,(640,480))
    #4-2.구역 내 객체 수 계산
    results=yolo_region(re_frame)#추론할 프레임 넣기
    #4-3.처리된 프레임 표시(show=False=>우리가 직접 창 띄움)
    cv2.imshow("REGION", results.plot_im)
    #4-4.q키를 눌러서 종료
    if cv2.waitKey(1) & 0xFF==ord('q'):
        print("q키를 눌러 종료")
        break
#5.자원 해제
cap.release()
cv2.destroyAllWindows()