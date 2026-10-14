def meters_to_feet(meters: float)-> float:
    """
    미터를 피트로 환산
    """
    return meters *3.28084   

while True:
    user_input = input("피트로 환산할 미터 값을 입력해주세요 : ")
    try:
        user_merters=float(user_input)
        feet=meters_to_feet(user_merters)
        print(f"{user_merters}m는 {feet}ft 입니다.")
        break
    except ValueError:
        print("숫자를입력해주세ㅛㅇ.다시 시도핫요")