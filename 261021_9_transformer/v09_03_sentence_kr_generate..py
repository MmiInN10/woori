from transformers import pipeline

#1.텍스트 생성 파이프라인 생성
generator=pipeline("text-generation", model="skt/kogpt2-base-v2")

#2.시드 문장 입력(이어 쓸 첫 부분)
q=input("이어서 쓸 첫 문장을 입력해주세요 : ")

#3.텍스트 생성 실행
results=generator(
    q,
    max_new_tokens=50,  #추가 생성할 토큰 수(길수록 추론 시간도 길어짐)
    num_return_sequences=1,  #반환 문장 1개로 설정
    
)

#4.결과 출력
print(results[0]["generated_text"])
'''
이어서 쓸 첫 문장을 입력해주세요 : 너는 뭐든 될 수 있지만,
너는 뭐든 될 수 있지만, 그게 쉽지가 않다.
그래서 나는 여러 가지 노력을 기울이지만 내게는 아무 것도 없다.
그냥 다 포기해 버린다.
그래서 나는 그게 제일 어려운 일이라 생각한다.
이런 생각을 했었다.
아무 것도 할 수 없는 일, 할 수 없는 일을
'''
