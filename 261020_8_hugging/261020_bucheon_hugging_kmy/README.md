# AI 변명 생성기
상황과 말투를 고르면 변명을 만들고, 분위기에 맞는 사과문 이미지까지 써 주는 서비스입니다.

- 상황 입력 → 말투 선택 → 제목, 본문, 추신이 있는 사과문 생성
- 말투마다 다른 손글씨 폰트와 편지지(종이색, 질감)로 이미지를 만들어 줍니다.
- 말투: 진지, 강아지, 애교, 로봇, 사극

## 사용 모델
| 용도 | 모델 |
|---|---|
| 변명과 사과문 글 생성 | `Qwen/Qwen2.5-72B-Instruct` (Hugging Face Inference Providers) |
| 사과문 이미지 | AI 모델 없이 Pillow로 합성 (`fonts/`의 손글씨 폰트) |

## 폴더 구조
```
261020_bucheon_hugging_kmy/
├── app.py            # Gradio 앱 (실행 파일)
├── fonts/            # 말투별 손글씨 폰트 (.ttf)
├── requirements.txt  # 필요 라이브러리
├── .env.example      # 토큰 입력 양식
└── README.md
```

## 사전 준비: Hugging Face 토큰
1. huggingface.co → Settings → Access Tokens에서 토큰을 만듭니다.
2. Fine-grained 토큰이라면 **"Make calls to Inference Providers"** 권한을 체크해야 합니다. (없으면 403 오류가 납니다.)

## 실행 방법
```bash
# 1. 가상환경 (선택)
python -m venv .venv
.venv\Scripts\activate

# 2. 라이브러리 설치
pip install -r requirements.txt

# 3. 토큰 설정 (택 1)
#   방법 A: .env.example 을 .env 로 복사한 뒤 HF_TOKEN 입력
copy .env.example .env
#   방법 B: .env 없이 실행하면 터미널에서 토큰을 입력받습니다. (입력은 화면에 보이지 않음)

# 4. 실행
python app.py
```
브라우저에서 `http://127.0.0.1:7860` 으로 접속합니다.

## 사용법
1. "어떤 상황인가요?"에 상황을 적습니다. (50자 이내, 예: 학원에 30분 지각했어요)
2. 말투를 고릅니다.
3. 이름은 선택입니다. 비우면 서명 없이 만들어집니다. (10자 이내)
4. Submit을 누르면 원문과 사과문 이미지가 나옵니다. 이미지는 오른쪽 위 버튼으로 저장할 수 있습니다.

같은 입력도 누를 때마다 결과가 달라지니 마음에 드는 걸 골라 보세요.

## 폰트 출처
Google Fonts의 SIL Open Font License 폰트를 사용했습니다.
Nanum Myeongjo, Song Myung, Nanum Gothic Coding, Gaegu, Hi Melody