
with open("2026-10-13.jpg", 'rb') as f:
    photo_data=f.read()
print(photo_data)

with open("memo.txt", "a", encoding="utf-8") as f:
    f.write("새로운 한 줄 추가")

with open("memo.txt", "r", encoding="utf-8") as f:
    text=f.read()
print(text)

print("입력할 내용을 적어라")
user_input =input()
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write(user_input)
    f.write("작성된 내용:")
with open("memo.txt", "r", encoding="utf-8")as f:
    text=f.read()
print(text)

with open("memo2.txt", "x", encoding="utf-8")as f:
    f.write("새로운 x옵션")
