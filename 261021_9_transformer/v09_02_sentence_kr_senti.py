from transformers import pipeline

#1.감정 분석 파이프라인 생성
classifier=pipeline("sentiment-analysis", model="matthewburke/korean_sentiment")

#2.분석할 문장 입력
text="짜증나"


#3.문장 분석
results=classifier(text)

#4.결과 확인
sentiment = "POSITIVE" if results[0]['label'] == "LABEL_1" else "NEGATIVE"
print(f"문장 분석 결과 : {sentiment}")
print(f"문장 분석 점수 : {results[0]['score']:.4f}")    # 1에 가까울수록 모델 확신도 높음
#출력
# 문장 분석 결과 : NEGATIVE
# 문장 분석 점수 : 0.9367
