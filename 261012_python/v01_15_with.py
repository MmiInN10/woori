# 파일 쓰기: 새로 생성, 기존 내용 덮어씀
# with open("memo.txt", "w", encoding="utf-8") as f:
#     f.write("새로운 한 줄 추가")
    
    
# 파일 읽기
# with open("memo.txt", "r", encoding="utf-8") as f:
#     text=f.read()    

#파일 이어 쓰기
with open("memo.txt", "a", encoding="utf-8") as f:
    f.write("\n지금 내가 쓴 내용도 작성 완료하자\n")
print("완료")