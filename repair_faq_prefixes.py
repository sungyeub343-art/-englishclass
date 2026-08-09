from pathlib import Path
import json
import re

ROOT = Path(r"c:\Users\M\Desktop\회화")

CH_TITLE = re.compile(r"<title>(?P<prefix>.+?) 중국어회화 .*?</title>")
JP_TITLE = re.compile(r"<title>(?P<prefix>.+?) 일본어회화 .*?</title>")
FAQ_BLOCK_RE = re.compile(
    r'<section class="detail faq-section" style="padding-top:8px">.*?</section>\s*<section class="detail" style="padding-top:4px">.*?</section>',
    re.S,
)
SCHEMA_RE = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)
IMG_RE = re.compile(r'<img src="\[복사본\] 파워잉글리시\.jpg"[^>]*>')


def build_faq_html(prefix: str, lang: str, parent_name: str) -> str:
    if lang == "chinese":
        return f'''<section class="detail faq-section" style="padding-top:8px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">{prefix} 중국어회화 자주 묻는 질문</h2>
    <div style="display:grid;gap:12px">
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">초보자도 수업을 시작할 수 있나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">네. 왕초보부터 직장인까지 수준별로 발화량과 복습량을 조절해 {prefix} 중국어회화 수업을 맞춤 설계합니다.</p>
      </article>
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">여행회화와 실무회화 중 무엇을 먼저 준비해야 하나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">목표에 따라 다르지만, 여행회화는 상황별 패턴 훈련, 실무회화는 업무 표현과 말하기 속도 조절이 핵심입니다.</p>
      </article>
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">무료 레벨테스트는 꼭 받아야 하나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">무료 레벨테스트를 받으면 현재 수준과 목표를 바탕으로 {prefix} 중국어회화 수업 방향을 더 정확히 설정할 수 있습니다.</p>
      </article>
    </div>
  </div>
</section>
<section class="detail" style="padding-top:4px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">관련 페이지 바로가기</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="{parent_name}">{prefix} 관련 지역 페이지</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="chinese.html">중국어회화 전체 지역 보기</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="index.html#apply">무료 레벨테스트 신청</a>
    </div>
  </div>
</section>'''

    return f'''<section class="detail faq-section" style="padding-top:8px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">{prefix} 일본어회화 자주 묻는 질문</h2>
    <div style="display:grid;gap:12px">
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">초보자도 수업을 시작할 수 있나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">네. 왕초보부터 직장인까지 수준별로 발음, 문장 구성, 복습량을 조절해 {prefix} 일본어회화 수업을 맞춤 설계합니다.</p>
      </article>
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">여행회화와 비즈니스회화 중 무엇을 먼저 준비해야 하나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">여행회화는 상황별 패턴 훈련이, 비즈니스회화는 업무 표현과 말하기 속도 조절이 중요합니다.</p>
      </article>
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">무료 레벨테스트는 꼭 받아야 하나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">무료 레벨테스트를 받으면 현재 수준과 목표를 바탕으로 {prefix} 일본어회화 수업 방향을 더 정확히 설정할 수 있습니다.</p>
      </article>
    </div>
  </div>
</section>
<section class="detail" style="padding-top:4px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">관련 페이지 바로가기</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="{parent_name}">{prefix} 관련 지역 페이지</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="japanese.html">일본어회화 전체 지역 보기</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="index.html#apply">무료 레벨테스트 신청</a>
    </div>
  </div>
</section>'''


def build_schema(prefix: str, lang: str, path: Path, description: str) -> str:
    name = f"{prefix} {'중국어회화' if lang == 'chinese' else '일본어회화'} 1:1 화상 스피킹 수업"
    faq2 = "여행회화와 실무회화 중 무엇을 먼저 준비해야 하나요?" if lang == "chinese" else "여행회화와 비즈니스회화 중 무엇을 먼저 준비해야 하나요?"
    answer1 = (
        f"네. 왕초보부터 직장인까지 수준별로 발화량과 복습량을 조절해 {prefix} 중국어회화 수업을 맞춤 설계합니다."
        if lang == "chinese"
        else f"네. 왕초보부터 직장인까지 수준별로 발음, 문장 구성, 복습량을 조절해 {prefix} 일본어회화 수업을 맞춤 설계합니다."
    )
    answer2 = (
        "목표에 따라 다르지만, 여행회화는 상황별 패턴 훈련, 실무회화는 업무 표현과 말하기 속도 조절이 핵심입니다."
        if lang == "chinese"
        else "여행회화는 상황별 패턴 훈련이, 비즈니스회화는 업무 표현과 말하기 속도 조절이 중요합니다."
    )
    payload = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "url": f"https://englishclass.kr/{path.name}",
        "description": description,
        "inLanguage": "ko-KR",
        "publisher": {"@type": "Organization", "name": "파워잉글리쉬", "url": "https://englishclass.kr/"},
        "mainEntity": {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "초보자도 수업을 시작할 수 있나요?",
                    "acceptedAnswer": {"@type": "Answer", "text": answer1},
                },
                {
                    "@type": "Question",
                    "name": faq2,
                    "acceptedAnswer": {"@type": "Answer", "text": answer2},
                },
            ],
        },
    }
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + '</script>'


def update(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lang = "chinese" if path.name.startswith("chinese-") else "japanese"
    match = (CH_TITLE if lang == "chinese" else JP_TITLE).search(text)
    if not match:
        return False

    prefix = match.group("prefix")
    description = (
        f"{prefix} 중국어회화, 중국어 스피킹, 발음 교정, 여행회화까지 1:1 화상 수업으로 맞춤 상담을 제공합니다."
        if lang == "chinese"
        else f"{prefix} 일본어회화, 일본어 스피킹, 발음 교정, 여행회화까지 1:1 화상 수업으로 맞춤 상담을 제공합니다."
    )

    parts = path.stem.split("-")
    parent_name = f"{parts[0]}-{parts[1]}.html" if len(parts) >= 3 else ("chinese.html" if lang == "chinese" else "japanese.html")
    if not (ROOT / parent_name).exists():
        parent_name = "chinese.html" if lang == "chinese" else "japanese.html"

    faq_new = build_faq_html(prefix, lang, parent_name)
    if FAQ_BLOCK_RE.search(text):
        text = FAQ_BLOCK_RE.sub(faq_new, text, count=1)
    elif '<section class="cta">' in text:
        text = text.replace('<section class="cta">', faq_new + '\n<section class="cta">', 1)

    schema_new = build_schema(prefix, lang, path, description)
    if SCHEMA_RE.search(text):
        text = SCHEMA_RE.sub(schema_new, text, count=1)
    elif '</head>' in text:
        text = text.replace('</head>', schema_new + '\n</head>', 1)

    alt_text = f"{prefix} {'중국어회화' if lang == 'chinese' else '일본어회화'} 수업 안내 이미지"
    img_match = IMG_RE.search(text)
    if img_match:
        img_tag = img_match.group(0)
        if ' alt=' in img_tag:
            new_tag = re.sub(r' alt=".*?"', f' alt="{alt_text}"', img_tag, count=1)
        else:
            new_tag = img_tag.replace('"', '"', 1)
            new_tag = img_tag[:-1] + f' alt="{alt_text}">'
        text = text.replace(img_tag, new_tag, 1)

    path.write_text(text, encoding="utf-8")
    return True


count = 0
for p in ROOT.glob("chinese-*.html"):
    if update(p):
        count += 1
for p in ROOT.glob("japanese-*.html"):
    if update(p):
        count += 1

print(f"Normalized: {count}")
