from ultralytics import YOLO

#1.모델 로드
model = YOLO("yolo11n.pt")
#현재는 파이토치 모델 로드임. 지금은 intel에 최적화된 모델을 불러와서 비교할거
#2.모델 내보내기
model.export(format="openvino")#intel CPU 최적화 모델
