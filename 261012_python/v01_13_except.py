user_input=input("피트로 환산할 미터 값을 입력해주세요 : ")

try:
    meters=int(user_input)
    feet=meters * 3.28084
    print(f"{meters}m는 {feet}ft입니다.")
except ValueError:
    print("숫자를 입력해주세요.") #숫자 외 값이 들어왔을 시 실행
