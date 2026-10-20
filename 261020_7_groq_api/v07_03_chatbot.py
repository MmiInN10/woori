from dotenv import load_dotenv  # .env 환경변수 설정
import os   # .env 파일 불러오기
from groq import Groq   # Groq API 사용
from termcolor import colored

#1.환경 변수 불러오기
load_dotenv()

#2.클라이언트 만들기(Groq API 요청)
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

#3.대화 기록 쌓음
messages=[] #메시지를 빈 리스트로 받아 대화 기록을 저장

#4.대화 진행 및 종료 입력 설정
while True:
    #4-1.질문
    q = input("나 : ")
    #4-2.종료 입력
    if q == "exit": #입력이 exit라면 종료
        print("대화를 종료합니다.")
        break
    #4-3.질문을 대화 기록에 추가
    messages.append(
        {
        "role":"user",
        "content":q
        }
    )
    #4-4.질문 보내기
    res=client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )
    #4-5.단변 받기(termcolor로 꾸며서 출력)
    answer=res.choices[0].message.content
    color_sentence=colored(answer, "red")
    print(f"AI는 말합니다 : {color_sentence}")
    
    #4-6.AI 답도 기록에 추가
    messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )