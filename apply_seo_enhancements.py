from pathlib import Path
import json
import re

ROOT = Path(r"c:\Users\M\Desktop\회화")


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


def build_schema(prefix: str, lang: str, url: str, description: str) -> str:
    if lang == "chinese":
        name = f"{prefix} 중국어회화 1:1 화상 스피킹 수업"
    else:
        name = f"{prefix} 일본어회화 1:1 화상 스피킹 수업"
    payload = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "url": url,
        "description": description,
        "inLanguage": "ko-KR",
        "publisher": {"@type": "Organization", "name": "파워잉글리쉬", "url": "https://englishclass.kr/"},
        "mainEntity": {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "초보자도 수업을 시작할 수 있나요?",
                    "acceptedAnswer": {"@type": "Answer", "text": f"네. 왕초보부터 직장인까지 수준별로 발화량과 복습량을 조절해 {prefix} {'중국어회화' if lang == 'chinese' else '일본어회화'} 수업을 맞춤 설계합니다."},
                },
                {
                    "@type": "Question",
                    "name": "여행회화와 실무회화 중 무엇을 먼저 준비해야 하나요?" if lang == "chinese" else "여행회화와 비즈니스회화 중 무엇을 먼저 준비해야 하나요?",
                    "acceptedAnswer": {"@type": "Answer", "text": "목표에 따라 다르지만, 여행회화는 상황별 패턴 훈련, 실무회화는 업무 표현과 말하기 속도 조절이 핵심입니다." if lang == "chinese" else "여행회화는 상황별 패턴 훈련이, 비즈니스회화는 업무 표현과 말하기 속도 조절이 중요합니다."},
                },
            ],
        },
    }
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + '</script>'


def apply(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if path.name.startswith("chinese-"):
        prefix_match = re.search(r"<title>(?P<prefix>.+?) 중국어회화 1:1 화상회화 무료상담 \| 파워잉글리쉬</title>", text)
        if not prefix_match:
            return False
        prefix = prefix_match.group("prefix")
        title = f"{prefix} 중국어회화 1:1 화상 스피킹 수업 | 무료 레벨테스트 | 파워잉글리쉬"
        description = f"{prefix} 중국어회화, 중국어 스피킹, 발음 교정, 여행회화까지 1:1 화상 수업으로 맞춤 상담을 제공합니다."
        og_title = f"{prefix} 중국어회화 1:1 화상 스피킹 수업"
        og_desc = f"{prefix} 지역 학습자에게 맞춘 중국어회화, 발음 교정, 여행회화, 무료 레벨테스트 상담 페이지입니다."
        lang = "chinese"
        alt_text = f"{prefix} 중국어회화 수업 안내 이미지"
    else:
        prefix_match = re.search(r"<title>(?P<prefix>.+?) 일본어회화 1:1 화상회화 무료상담 \| 파워잉글리쉬</title>", text)
        if not prefix_match:
            return False
        prefix = prefix_match.group("prefix")
        title = f"{prefix} 일본어회화 1:1 화상 스피킹 수업 | 무료 레벨테스트 | 파워잉글리쉬"
        description = f"{prefix} 일본어회화, 일본어 스피킹, 발음 교정, 여행회화까지 1:1 화상 수업으로 맞춤 상담을 제공합니다."
        og_title = f"{prefix} 일본어회화 1:1 화상 스피킹 수업"
        og_desc = f"{prefix} 지역 학습자에게 맞춘 일본어회화, 발음 교정, 여행회화, 무료 레벨테스트 상담 페이지입니다."
        lang = "japanese"
        alt_text = f"{prefix} 일본어회화 수업 안내 이미지"

    text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', text, count=1, flags=re.S)
    text = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{og_title}">', text, count=1, flags=re.S)
    text = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{og_desc}">', text, count=1, flags=re.S)

    if '<img src="[복사본] 파워잉글리시.jpg"' in text:
        text = text.replace('<img src="[복사본] 파워잉글리시.jpg"', f'<img src="[복사본] 파워잉글리시.jpg" alt="{alt_text}"', 1)

    stem = path.stem
    parts = stem.split('-')
    parent_name = f"{parts[0]}-{parts[1]}.html" if len(parts) >= 3 else ("chinese.html" if lang == "chinese" else "japanese.html")
    if not (ROOT / parent_name).exists():
        parent_name = "chinese.html" if lang == "chinese" else "japanese.html"

    if 'faq-section' not in text:
        text = text.replace('<section class="cta">', build_faq_html(prefix, lang, parent_name) + '\n<section class="cta">', 1)

    if 'application/ld+json' not in text:
        text = text.replace('</head>', build_schema(prefix, lang, f"https://englishclass.kr/{path.name}", description) + '\n</head>', 1)

    path.write_text(text, encoding='utf-8', newline='\n')
    return True


for pattern in ("chinese-*-*.html", "japanese-*-*.html"):
    updated = 0
    for path in ROOT.glob(pattern):
        if apply(path):
            updated += 1
    print(pattern, updated)
