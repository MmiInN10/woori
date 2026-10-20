import getpass
import json
import os
import random
import re

import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

load_dotenv()

TEXT_MODEL = "Qwen/Qwen2.5-72B-Instruct:deepinfra"
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

MAX_SITUATION = 50  # 상황 입력 글자수 제한
MAX_NAME = 10  # 이름 입력 글자수 제한

client = None  # main()에서 토큰을 받은 뒤 만든다

SYSTEM_PROMPT = """You write a fake apology letter that sounds formal and sincere, but is secretly a ridiculous excuse.
The writer never truly admits fault and blames absurd things (aliens, a pigeon, destiny, the weather...).
Given the user's situation and a tone, reply ONLY with this JSON (no other text):
{
  "title": "a short, funny apology-letter title, at most 12 Korean characters",
  "body": "at most 4 Korean sentences: start with an apology phrase, then the absurd excuse, and end with a fake pledge",
  "ps": "one short, funny Korean sentence added at the end as a postscript, without the word 추신"
}
Make it funny: the apology should be insincere or backfire (e.g. it ends up blaming the reader, or the pledge is absurd or contradicts itself).
Rules: write everything in Korean (Hangul only, no Chinese, Japanese, English, code or emoji) and fully commit to the tone."""

# 화면에 보이는 이름 -> LLM에게 전달할 말투 설명
TONES = {
    "진지": "an extreme 'T' (MBTI thinking type): zero empathy, cold logic and facts only, coldly points out that the apology is logically unnecessary, with a deadpan 'so what do you want me to do about it' attitude. Take inspiration from T-style retorts like '그래서 제가 뭘 어떻게 해야 하는데요?', '사과를 하면 시간이 돌아옵니까?', '감정적으로 접근하지 마시고 팩트만 보시죠.', but use at most one of them, rephrase it to fit the situation, and never mention numbers or facts that are not in the situation",
    "강아지": "a cute puppy, with barks like 멍멍 and 왈왈, and wagging-tail excitement",
    "애교": "super cute and aegyo-filled, baby talk with ~용, ~잉",
    "로봇": "a malfunctioning robot: glitchy, mechanical, with 삐빅 and ERROR messages",
    "사극": "a Joseon-dynasty historical drama, with endings like ~하옵니다, ~이옵니다, ~하노라",
}

# 말투별 편지지 스타일: 폰트, 종이색, 글자색, 줄 색
PAPERS = {
    "진지":   dict(font="NanumMyeongjo-Regular.ttf",     paper=(255, 253, 245), ink=(30, 30, 40),   line=(225, 222, 210)),
    "강아지": dict(font="Gaegu-Regular.ttf",             paper=(255, 244, 230), ink=(110, 60, 30),  line=(240, 220, 195), crumpled=True, paws=True),
    "애교":   dict(font="HiMelody-Regular.ttf",          paper=(255, 238, 244), ink=(200, 60, 110), line=(250, 212, 225)),
    "로봇":   dict(font="NanumGothicCoding-Regular.ttf", paper=(18, 24, 22),    ink=(90, 255, 140), line=(30, 52, 40)),
    "사극":   dict(font="SongMyung-Regular.ttf", paper=(240, 225, 195), ink=(40, 28, 20),   line=(220, 200, 165)),
}

WIDTH = 900
MARGIN = 80
LINE_H = 64
BODY_TOP = 230


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def clean(text):
    """폰트에 없는 이모지 등을 제거 (이미지에서 네모로 보이는 것 방지)."""
    return re.sub(r"[\U0001F000-\U0001FFFF☀-➿️]", lambda m: m.group(0) if m.group(0) in "♡★" else "", text).strip()


def wrap(text, font, max_width):
    """픽셀 너비를 기준으로 글자 단위 줄바꿈."""
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for ch in paragraph:
            if font.getlength(line + ch) > max_width:
                # 영어 단어가 중간에서 끊기지 않도록 단어째로 다음 줄로 넘김
                if ch.isascii() and ch.isalnum() and " " in line and line[-1].isascii() and line[-1].isalnum():
                    head, _, tail = line.rpartition(" ")
                    lines.append(head)
                    line = tail + ch
                else:
                    lines.append(line)
                    line = ch.lstrip()
            else:
                line += ch
        lines.append(line)
    return lines


def render_apology(title, body, ps, tone, name):
    style = PAPERS[tone]
    body_font = load_font(style["font"], 40)
    ps_font = load_font(style["font"], 34)
    small_font = load_font(style["font"], 34)

    # 제목이 길면 칸에 맞을 때까지 글자 크기를 줄인다
    title_size = 64
    title_font = load_font(style["font"], title_size)
    while title_size > 30 and title_font.getlength(title) > WIDTH - MARGIN * 2:
        title_size -= 4
        title_font = load_font(style["font"], title_size)

    text_width = WIDTH - MARGIN * 2
    body_lines = wrap(body, body_font, text_width)
    ps_lines = wrap(f"추신. {ps}", ps_font, text_width) if ps else []

    ps_top = BODY_TOP + LINE_H * len(body_lines) + 20
    footer_top = ps_top + 54 * len(ps_lines) + 40
    height = footer_top + (110 if name else 50)  # 이름이 없으면 서명 줄만큼 여백을 줄인다

    img = Image.new("RGB", (WIDTH, height), style["paper"])
    draw = ImageDraw.Draw(img)

    # 테두리와 줄
    draw.rectangle([24, 24, WIDTH - 24, height - 24], outline=style["ink"], width=3)
    for y in range(BODY_TOP + LINE_H - 8, ps_top, LINE_H):
        draw.line([MARGIN - 20, y, WIDTH - MARGIN + 20, y], fill=style["line"], width=2)

    # 종이 질감 (글씨보다 먼저 입혀서 글씨는 선명하게 유지)
    if style.get("paws"):
        scatter_paws(img, (120, 75, 40))
    if style.get("crumpled"):
        img = crumple(img)
        draw = ImageDraw.Draw(img)

    # 제목
    tw = draw.textlength(title, font=title_font)
    draw.text(((WIDTH - tw) / 2, 150 - title_size), title, font=title_font, fill=style["ink"])
    draw.line([MARGIN, 190, WIDTH - MARGIN, 190], fill=style["ink"], width=3)

    # 본문 (줄마다 아주 살짝 흔들어 손글씨 느낌)
    for i, line in enumerate(body_lines):
        draw.text((MARGIN + random.randint(-2, 2), BODY_TOP + i * LINE_H), line, font=body_font, fill=style["ink"])

    # 추신
    for i, line in enumerate(ps_lines):
        draw.text((MARGIN, ps_top + i * 54), line, font=ps_font, fill=style["ink"])

    # 서명 (이름을 입력했을 때만)
    if name:
        sign = f"{name} 올림"
        draw.text((WIDTH - MARGIN - draw.textlength(sign, font=small_font), footer_top), sign, font=small_font, fill=style["ink"])
    return img


def crumple(img):
    """구겨진 종이 느낌: 면 단위 명암 + 주름선 + 잔 노이즈를 overlay로 입힌다."""
    w, h = img.size
    shade = Image.new("L", (w, h), 128)
    d = ImageDraw.Draw(shade)
    for _ in range(45):  # 구겨진 면
        pts = [(random.randint(-50, w + 50), random.randint(-50, h + 50)) for _ in range(3)]
        d.polygon(pts, fill=random.randint(85, 175))
    shade = shade.filter(ImageFilter.GaussianBlur(7))
    d = ImageDraw.Draw(shade)
    for _ in range(35):  # 주름선 (어두운 선 옆에 밝은 선)
        x, y = random.randint(0, w), random.randint(0, h)
        pts = [(x, y)]
        for _ in range(random.randint(2, 4)):
            x += random.randint(-160, 160)
            y += random.randint(-160, 160)
            pts.append((x, y))
        d.line(pts, fill=40, width=random.randint(2, 4))
        d.line([(px + 3, py + 3) for px, py in pts], fill=225, width=2)
    shade = shade.filter(ImageFilter.GaussianBlur(1.3))
    shade = ImageChops.add(shade, Image.effect_noise((w, h), 16), scale=1, offset=-128)
    return ImageChops.overlay(img, shade.convert("RGB"))


def paste_paw(img, cx, cy, size, angle, color, alpha=70):
    """강아지 발바닥 하나 (큰 패드 1개 + 발가락 4개)를 회전해서 붙인다."""
    s = size
    tile = Image.new("RGBA", (s * 3, s * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    fill = (*color, alpha)
    c = s * 1.5
    d.ellipse([c - s * 0.55, c - s * 0.1, c + s * 0.55, c + s * 0.7], fill=fill)  # 큰 패드
    for dx, dy, r in [(-0.62, -0.25, 0.22), (-0.22, -0.62, 0.24), (0.22, -0.62, 0.24), (0.62, -0.25, 0.22)]:
        d.ellipse([c + dx * s - r * s, c + dy * s - r * s, c + dx * s + r * s, c + dy * s + r * s], fill=fill)
    tile = tile.rotate(angle, resample=Image.BICUBIC)
    img.paste(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)


def scatter_paws(img, color):
    """발바닥이 종이 위를 걸어간 것처럼 지그재그로 찍는다."""
    w, h = img.size
    y, left = h - 60, True
    while y > 120:
        x = w * (0.2 if left else 0.32) + random.randint(-20, 20)
        paste_paw(img, x, y, random.randint(26, 34), random.randint(-25, 25), color)
        left = not left
        y -= random.randint(95, 125)


def parse_letter(raw):
    """LLM 응답에서 title/body/ps를 꺼낸다. JSON이 아니면 전체를 본문으로 쓴다."""
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        data = json.loads(match.group(0))
        return clean(data["title"]), clean(data["body"]), clean(data.get("ps", ""))
    except (AttributeError, json.JSONDecodeError, KeyError):
        return "사과문", clean(raw), ""


def make_apology(situation, tone, name):
    situation = situation.strip()[:MAX_SITUATION]
    name = name.strip()[:MAX_NAME]
    if not situation:
        raise gr.Error("상황을 입력해주세요!")

    try:
        completion = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Situation: {situation}\nTone: {TONES[tone]}"},
            ],
            temperature=0.7,
        )
    except Exception as e:
        print(f"[LLM 호출 실패] {e}")
        raise gr.Error("AI 호출에 실패했어요. 토큰 권한이나 네트워크를 확인하고 다시 시도해주세요.")

    title, body, ps = parse_letter(completion.choices[0].message.content)
    original = f"[{title}]\n{body}" + (f"\n추신. {ps}" if ps else "")
    return original, render_apology(title, body, ps, tone, name)


demo = gr.Interface(
    fn=make_apology,
    inputs=[
        gr.Textbox(label=f"어떤 상황인가요? (최대 {MAX_SITUATION}자)", placeholder="예: 학원에 30분 지각했어요", max_length=MAX_SITUATION),
        gr.Dropdown(list(TONES), value="진지", label="말투"),
        gr.Textbox(label=f"이름 (선택, 최대 {MAX_NAME}자)", placeholder="예: 김민영", max_length=MAX_NAME),
    ],
    outputs=[gr.Textbox(label="원문"), gr.Image(label="사과문 이미지")],
    title="AI 변명 생성기",
    description="상황과 말투를 고르면 변명을 만들고, 분위기에 맞는 사과문까지 써 드립니다.",
    flagging_mode="never",
)


def main():
    global client
    token = os.environ.get("HF_TOKEN") or getpass.getpass("HF 토큰을 입력하세요 (입력은 화면에 보이지 않습니다): ")
    client = InferenceClient(api_key=token)
    demo.launch()


if __name__ == "__main__":
    main()
