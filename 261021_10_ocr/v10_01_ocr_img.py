import pytesseract      #OCR사용
from PIL import Image   #이미지 처리 도구
import os
import easyocr

# # 1.Tesseract 실행 파일 경로 지정
# pytesseract.pytesseract.tesseract_cmd="c:/Program Files/Tesseract-OCR/tesseract.exe"
# #ㅈ. 이미지 물러오기
# image=Image.open("261021_10_ocr\input3.jpg")
# #3.OCR 수행
# results=pytesseract.image_to_string(
#     image,
#     lang="eng+kor"  #영어와 한글 동시 읽기
# )
# #4.결과 출력
# print(f"OCR 실행 결과 : {results}")
'''
OCR 실행 결과 : This is a lot of 12 point text to test the
ocr code and see if it works on all types
of file format.

The quick brown dog jumped over the
lazy fox. The quick brown dog jumped
over the lazy fox. The quick brown dog
jumped over the lazy fox. The quick
brown dog jumped over the lazy fox.
'''

'''
OCR 실행 결과 : Ｌ스트스때스56<1때 

이수진

팀장 / 제품개발팀

+123-456-7890
1『6110@「62117/8「620[5166.0007
123 40616 56, 407 다, 51 12345
'''

'''
OCR 실행 결과 : LARANASKIN

이수진

팀장 / 제 품 개발팀

+123-456-7890
hello@reallygreatsite.com
123 Anywhere St., Any City, ST 12345
'''
#번호판 이미지 인식
#2.다른 ORY비교

reader = easyocr.Reader(['ko', 'en'])
results = reader.readtext("261021_10_ocr/input4.jpg")
for box, text, conf in results:
    print(text)
''' 
30고
9703
CEVRDLEI
EOUINUX
RwD
FIEmED
'''

