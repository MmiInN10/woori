from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

#1.모델 로드
#1.모델 로드
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
#다국어(한국어 포함) 문장 임베딩 모델

sen1="고양이가 소파에서 자고 있다"
sen2="고양이가 침대에서 낮잠잔다"


#3. 문장 -> 숫자 좌표로 바꾸기(인코딩)
emb1=model.encode(sen1, convert_to_tensor=True)
emb2=model.encode(sen2, convert_to_tensor=True)
#4.두 문장 유사도 측정 (코사인 유사도)
cos_sim=util.pytorch_cos_sim(emb1,emb2)

#5.결과 출력
print(f"두 문장의 유사도 : {cos_sim.item():.4f}")