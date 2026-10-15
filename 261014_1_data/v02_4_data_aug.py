import cv2
import matplotlib.pyplot as plt

#1.이미지 로드
img=cv2.imread("261014_1_data/2026-10-13.jpg")

#이미지 증강
img_bright=cv2.convertScaleAbs(img, alpha=1, beta=50)
#alpha: 픽셀에 곱하는 값
#beta: 더할 밝기(+50=밝게, -50=어둡게)

#채도
img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
h,s,v=cv2.split(img_hsv)
h=(h+30)%100
#채도 범위 변경
img_hue=cv2.cvtColor(cv2.merge([h,s,v]),cv2.COLOR_HSV2BGR)

#3. 이미지 시각화
fig, ax=plt.subplots(2,2, figsize=(10,5))#전체 표 사이즈 2열 2행?

#3-1.원본 이미지
ax[0,0].imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
ax[0,0].axis('off')
ax[0,0].set_title("Original")#제목 넣기

#3-2.밝기 이미지
ax[0,1].imshow(cv2.cvtColor(img_bright,cv2.COLOR_BGR2RGB))
ax[0,1].axis('on')
ax[0,1].set_title("Bright")#제목 넣기

#3-3.상하 반전 이미지
img_flip = cv2.flip(img, 0)
#1: 수평, 0: 수직, -1: 수평, 수직
ax[1,0].imshow(cv2.cvtColor(img_flip, cv2.COLOR_BGR2RGB))
ax[1,0].axis('on')
ax[1,0].set_title("flip")#제목 넣기

#3-4. 채도 변경 이미지
ax[1,1].imshow(cv2.cvtColor(img_hue,cv2.COLOR_BGR2RGB))
ax[1,1].axis('off')
ax[1,1].set_title("HSV")#제목 넣기

#4.그림창 띄우기
plt.show()

#이미지 저장
cv2.imwrite("./bright_img.jpg", img_bright)
cv2.imwrite("./bright_img.jpg", img_hue)
cv2.imwrite("./bright_img.jpg", img_flip)
print("이미지 저장 완료")