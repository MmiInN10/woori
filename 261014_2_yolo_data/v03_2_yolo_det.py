from ultralytics import YOLO
import cv2
#1.모델 로드
#2.모델 추론
model = YOLO("yolo11m.pt")
result=model("C:/Users/Woori/Desktop/woori/input/input_video.mp4")
#3.결과 시각화
result_image=result[0].plot()
#4.결과 이미지 저장
#기존 방식
#output_path="./output_dat.jpg"
#cv2.imwrite("./output_det.jpg", result_image)
cv2.imwrite("./output_det.jpg", result_image)

print("결과 이미지 잘 저장 됐습니다!!")