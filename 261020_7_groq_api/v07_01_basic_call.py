#pip install groq
#pip install python-dotenv
from groq import Groq
from dotenv import load_dotenv # .env읽는 도구
import os

#1. .env의 GROQ_API_KEY를 환경변수로 불러옴
load_dotenv()

#2. 키로 Groq 클라이언트 만들기(키를 통해서 요청)
client=Groq(api_key=os.getenv("GROQ_API_KEY")) #코드 노출 없이 환경변수명으로 불러오기

#3. 질문 보내기
res = client.chat.completions.create(
    model="openai/gpt-oss-20b", #무료, 빠른 가성비 모델
    messages=[
        {
            "role":"user",  #질문이나 요청할때
            "content":"groq만의 차별점 5가지를 한글로 대답해라."   #질문
        }
    ]
)

#4. 답변 받기
result=res.choices[0].message.content
print(f"API의 답변 : {result} \n======================================)")