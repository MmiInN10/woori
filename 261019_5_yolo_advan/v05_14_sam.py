from ultralytics import SAM
import time
import cv2
#1.모델 로드
model=SAM("sam_b.pt")
#sam_b(빠름), sam_l(정확,느림)
#2.이미지 경로 설정
image_path="261019_5_yolo_advan/pexels-alonzo-photo-2765040-6678136.jpg"
#이미지 읽기
input_image=cv2.imread(image_path)
#이미지 리사이즈
re_input_image=cv2.resize(input_image,(197,236))
#3.추론 시간 측정 시작
start_time=time.time()
#4.모델 추론
# model(re_input_image,save=True,show_boxes=False)#추론 결과 저장
results=model(re_input_image)#추론 결과 저장
#5.추론 시간 측정 종료
end_time=time.time()
#f라벨 제거
no_label_output=results[0].plot(labels=False,boxes=False)

#저장
cv2.imwrite("./output_sam.jpg",no_label_output)
#6.결과 로그 출력
if_time=end_time-start_time
print(f"총 추론 시간:{if_time:.2f}")
print("추론 완료")