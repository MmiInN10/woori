from ultralytics import FastSAM
import cv2
#1.이미지 경로
source="261019_5_yolo_advan/pexels-artem-makarov-289670876-15820828.jpg"
#2.모델 로드
model=FastSAM("FastSAM-s.pt")
#s(소형 모델),x(대형 모델)
#3.모델 추론
results=model(source,texts="cat")#텍스트로 고양이만 탐지하도록 설정
#4.결과 이미지 가져오기
output_path="./output_result.jpg"
output_image=results[0].plot()
#5.결과 이미지 저장
cv2.imwrite(output_path,output_image)
#6.실행 출력 로그
print("코드 실행 완료")