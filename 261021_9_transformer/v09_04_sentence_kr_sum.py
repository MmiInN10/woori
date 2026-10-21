from transformers import pipeline
#pip install transformers==5.20.2
#다운그레이드
#pip uninstall transformers
#pip install transformers==4.46.3

#1.요약 파이프라인
summarizer=pipeline("summarization", model="eenzeenee/t5-base-korean-summarization")

#2요약할 원문(영어단락)
text="""네가 바라보는 세상이란
성냥갑처럼 조그맣고
바삐 움직이는 사람들
허전한 맘으로 돈을 세도
네겐 아무 의미 없겠지
날아오를 하늘이 있으니
너는 알고 있지 구름의 숲
우린 보지 않는 노을의 냄새
바다 건너 피는 꽃의 이름
옛 방랑자의 노래까지
네겐 모두 의미 있겠지
날아오를 하늘이 있으니
내려오지마 이 좁고 우스운 땅 위에
내려오지마 네 작은 날개를 쉬게 할 곳은 없어
어느 날 네가 날개를 다쳐
거리 가운데 동그랗게 서서
사람들이라도 믿고 싶어
조용한 눈으로 바라보며
“내겐 아무 힘이 없어요
날아오를 하늘이 멀어요”
내려오지마 이 좁고 우스운 땅 위에
내려오지마 네 작은 날개를 쉬게 할 곳은 없어
가장 아름다운 하늘 속
멋진 바람을 타는 너는
눈부시게 높았고 외로웠지만
가야 한다면 어딘가 묻히고 싶다면
우리가 없는 평화로운 곳으로 가서
"""

#3.요약 실행
summary=summarizer(
    "summarize: " + text,   #이 모델은 접두어가 필요합니다
    min_length=20,
    max_length=100,
    do_sample=False
)

#4.결과 확인
sum_text=summary[0]["summary_text"]
print(f"요약된 문장:{sum_text}")
#요약된 문장:세상이란 성냥갑처럼 조그맣고 바삐 움직이는 사람들 쓸쓸한 맘으로 돈을 세도 네겐 아무 의미 없을 것이다.