from transformers import pipeline
from deep_translator import MyMemoryTranslator

#영어 -> 한국어 번역 함수 
def trans_en_to_ko(sum_en_text:str)-> str:
    '''
    주어진 영어 문장을 한국어로 변역하는 함수
    '''
    sum_ko_text = MyMemoryTranslator(source="en-US", target="ko-KR").translate(sum_en_text)
    return sum_ko_text

#추가 pip install deep-translator
#pip install transformers==5.20.2
#다운그레이드
#pip uninstall transformers
#pip install transformers==4.46.3

#1.요약 파이프라인
summarizer=pipeline("summarization", model="t5-small")

#2요약할 원문(영어단락)
text="""I've been defeated and brought down
Dropped to my knees when hope ran out
The time has come to change my ways
On this day I see clearly everything has come to life
A bitter place and a broken dream
And we'll leave it all, leave it all behind
I'll never long for what might have been
And now regret won't waste my life again
I won't look back
I'll fight to remain
On this day I see clearly everything has come to life
A bitter place and a broken dream
And we'll leave it all behind
On this day it's so real to me
Everything has come to life
Another chance to chase a dream
Another chance to feel 
Chance to feel alive
Fear will kill me, all I could be
Lift these sorrows
Let me breathe, could you set me free
Could you set me free
On this day I see clearly everything has come to life
A bitter place and a broken dream
And we'll leave it all behind
On this day it's so real to me
Everything has come to life
Another chance to chase a dream
Another chance to feel 
Chance to feel alive
"""

#3.요약 실행
summary=summarizer(
    text,   #요약할문장
    min_length=20,   #최소 토큰 수
    max_length=100, #최대 토큰 수
    do_sample=False #매번 동일 결과 출력
)

#4.결과 확인
sum_en_text=summary[0]["summary_text"]
#print(f"요약된 문장:{sum_en_text/))/
#요약된 문장:I've been defeated and brought down Dropped to my knees when hope ran out The time has come to change my ways On this day I see clearly everything has come . to life A bitter place and a broken dream And we'll leave it all behind I'll never long for what might have been And now regret won't waste my life again I will fight to remain on this day .
#요약된 문장:나는 패배했고 무너져 내렸다. 희망이 사라졌을 때 무릎을 꿇고 말았다. 이제는 삶의 방식을 바꿔야 할 때가 왔다. 오늘, 나는 모든 것이 다시 살아나는 것을 분명히 본다. 쓰라린 현실과 산산조각 난 꿈, 이제 그 모든 것을 뒤로하려 한다. 이루어질 수도 있었던 일들을 더는 그리워하지 않을 것이며, 이제는 후회로 내 삶을 낭비하지도 않을 것이다. 오늘, 나는 이 자리를 지키기 위해 싸울 것이다.
sum_ko_text=trans_en_to_ko(sum_en_text)
print(f"### 한국어 변역 후 요약된 문장:{sum_ko_text}")

#5.한글 번역
# kr_text = trans_en_to_ko(sum_en_text)
# print(f"번역된 문장:{kr_text}")

##과제
# 결과 확인 => 영어 => 번역 => 한굴어로 출력