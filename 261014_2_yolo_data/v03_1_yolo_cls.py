from ultralytics import YOLO
import cv2

# 1. 모델로드
# YOLO("모델명")
model=YOLO("yolo11n-cls.pt")
#n->s->m->1->x(model size)

# 2. 모델 추론
result = model("C:/Users/Woori/Desktop/woori/input3.jpg") #상대경로

# 3. 결과 시각화
result_image=result[0].plot()

# 4. 결과 이미지 저장
# output_result_image_path="저장할경로/저장할이미지파일이름.jpg"
output_result_image_path = "./output3.jpg"
cv2.imwrite(output_result_image_path, result_image)

print(f"예측 결과 이미지가 잘 저장 되었습니다. {output_result_image_path}")