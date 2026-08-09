from pathlib import Path
import json
import re

ROOT = Path(r"c:\Users\M\Desktop\회화")

for path in sorted(ROOT.glob("*.html")):
    if not (path.name.startswith("chinese-") or path.name.startswith("japanese-")):
        continue
    text = path.read_text(encoding="utf-8")
    if 'faq-section' in text or 'application/ld+json' in text:
        continue
    if path.name.startswith("chinese-"):
        region = path.name.replace("chinese-", "").replace(".html", "")
        title_prefix = region.replace('-', ' ')
        faq_title = f"{title_prefix} 중국어회화 자주 묻는 질문"
        schema_name = f"{title_prefix} 중국어회화 1:1 화상 스피킹 수업"
        alt_text = f"{title_prefix} 중국어회화 수업 안내 이미지"
        parent_href = "chinese.html"
        if region.startswith("busan"):
            parent_href = "chinese-busan.html"
        elif region.startswith("chungbuk"):
            parent_href = "chinese-chungbuk.html"
        elif region.startswith("chungnam"):
            parent_href = "chinese-chungnam.html"
        elif region.startswith("daegu"):
            parent_href = "chinese-daegu.html"
        elif region.startswith("daejeon"):
            parent_href = "chinese-daejeon.html"
        elif region.startswith("gangwon"):
            parent_href = "chinese-gangwon.html"
        elif region.startswith("gwangju"):
            parent_href = "chinese-gwangju.html"
        elif region.startswith("gyeongbuk"):
            parent_href = "chinese-gyeongbuk.html"
        elif region.startswith("gyeonggi"):
            parent_href = "chinese-gyeonggi.html"
        elif region.startswith("gyeongnam"):
            parent_href = "chinese-gyeongnam.html"
        elif region.startswith("incheon"):
            parent_href = "chinese-incheon.html"
        elif region.startswith("jeju"):
            parent_href = "chinese-jeju.html"
        elif region.startswith("jeonbuk"):
            parent_href = "chinese-jeonbuk.html"
        elif region.startswith("jeonnam"):
            parent_href = "chinese-jeonnam.html"
        elif region.startswith("sejong"):
            parent_href = "chinese-sejong.html"
        elif region.startswith("seoul"):
            parent_href = "chinese-seoul.html"
        faq_html = f'''<section class="detail faq-section" style="padding-top:8px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">{faq_title}</h2>
    <div style="display:grid;gap:12px">
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">초보자도 수업을 시작할 수 있나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">네. 왕초보부터 직장인까지 수준별로 발화량과 복습량을 조절해 {title_prefix} 중국어회화 수업을 맞춤 설계합니다.</p>
      </article>
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">여행회화와 실무회화 중 무엇을 먼저 준비해야 하나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">목표에 따라 다르지만, 여행회화는 상황별 패턴 훈련, 실무회화는 업무 표현과 말하기 속도 조절이 핵심입니다.</p>
      </article>
    </div>
  </div>
</section>
<section class="detail" style="padding-top:4px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">관련 페이지 바로가기</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="{parent_href}">{title_prefix} 관련 지역 페이지</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="chinese.html">중국어회화 전체 지역 보기</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="index.html#apply">무료 레벨테스트 신청</a>
    </div>
  </div>
</section>'''
        schema_payload = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": schema_name,
            "url": f"https://englishclass.kr/{path.name}",
            "description": f"{title_prefix} 중국어회화, 중국어 스피킹, 발음 교정, 여행회화까지 1:1 화상 수업으로 맞춤 상담을 제공합니다.",
            "inLanguage": "ko-KR",
            "publisher": {
                "@type": "Organization",
                "name": "파워잉글리쉬",
                "url": "https://englishclass.kr/",
            },
            "mainEntity": {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "초보자도 수업을 시작할 수 있나요?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"네. 왕초보부터 직장인까지 수준별로 발화량과 복습량을 조절해 {title_prefix} 중국어회화 수업을 맞춤 설계합니다.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "여행회화와 실무회화 중 무엇을 먼저 준비해야 하나요?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "목표에 따라 다르지만, 여행회화는 상황별 패턴 훈련, 실무회화는 업무 표현과 말하기 속도 조절이 핵심입니다.",
                        },
                    },
                ],
            },
        }
        schema = '<script type="application/ld+json">' + json.dumps(schema_payload, ensure_ascii=False) + '</script>'
    else:
        region = path.name.replace("japanese-", "").replace(".html", "")
        title_prefix = region.replace('-', ' ')
        faq_title = f"{title_prefix} 일본어회화 자주 묻는 질문"
        schema_name = f"{title_prefix} 일본어회화 1:1 화상 스피킹 수업"
        alt_text = f"{title_prefix} 일본어회화 수업 안내 이미지"
        parent_href = "japanese.html"
        if region.startswith("busan"):
            parent_href = "japanese-busan.html"
        elif region.startswith("chungbuk"):
            parent_href = "japanese-chungbuk.html"
        elif region.startswith("chungnam"):
            parent_href = "japanese-chungnam.html"
        elif region.startswith("daegu"):
            parent_href = "japanese-daegu.html"
        elif region.startswith("daejeon"):
            parent_href = "japanese-daejeon.html"
        elif region.startswith("gangwon"):
            parent_href = "japanese-gangwon.html"
        elif region.startswith("gwangju"):
            parent_href = "japanese-gwangju.html"
        elif region.startswith("gyeongbuk"):
            parent_href = "japanese-gyeongbuk.html"
        elif region.startswith("gyeonggi"):
            parent_href = "japanese-gyeonggi.html"
        elif region.startswith("gyeongnam"):
            parent_href = "japanese-gyeongnam.html"
        elif region.startswith("incheon"):
            parent_href = "japanese-incheon.html"
        elif region.startswith("jeju"):
            parent_href = "japanese-jeju.html"
        elif region.startswith("jeonbuk"):
            parent_href = "japanese-jeonbuk.html"
        elif region.startswith("jeonnam"):
            parent_href = "japanese-jeonnam.html"
        elif region.startswith("sejong"):
            parent_href = "japanese-sejong.html"
        elif region.startswith("seoul"):
            parent_href = "japanese-seoul.html"
        faq_html = f'''<section class="detail faq-section" style="padding-top:8px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">{faq_title}</h2>
    <div style="display:grid;gap:12px">
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">초보자도 수업을 시작할 수 있나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">네. 왕초보부터 직장인까지 수준별로 발음, 문장 구성, 복습량을 조절해 {title_prefix} 일본어회화 수업을 맞춤 설계합니다.</p>
      </article>
      <article style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px">
        <h3 style="margin:0 0 8px;font-size:18px;">여행회화와 비즈니스회화 중 무엇을 먼저 준비해야 하나요?</h3>
        <p style="margin:0;color:var(--muted);line-height:1.7">여행회화는 상황별 패턴 훈련이, 비즈니스회화는 업무 표현과 말하기 속도 조절이 중요합니다.</p>
      </article>
    </div>
  </div>
</section>
<section class="detail" style="padding-top:4px">
  <div class="wrap">
    <h2 style="margin:0 0 14px;font-size:24px;">관련 페이지 바로가기</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="{parent_href}">{title_prefix} 관련 지역 페이지</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="japanese.html">일본어회화 전체 지역 보기</a>
      <a style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);font-weight:700" href="index.html#apply">무료 레벨테스트 신청</a>
    </div>
  </div>
</section>'''
        schema_payload = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": schema_name,
            "url": f"https://englishclass.kr/{path.name}",
            "description": f"{title_prefix} 일본어회화, 일본어 스피킹, 발음 교정, 여행회화까지 1:1 화상 수업으로 맞춤 상담을 제공합니다.",
            "inLanguage": "ko-KR",
            "publisher": {
                "@type": "Organization",
                "name": "파워잉글리쉬",
                "url": "https://englishclass.kr/",
            },
            "mainEntity": {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "초보자도 수업을 시작할 수 있나요?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"네. 왕초보부터 직장인까지 수준별로 발음, 문장 구성, 복습량을 조절해 {title_prefix} 일본어회화 수업을 맞춤 설계합니다.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "여행회화와 비즈니스회화 중 무엇을 먼저 준비해야 하나요?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "여행회화는 상황별 패턴 훈련이, 비즈니스회화는 업무 표현과 말하기 속도 조절이 중요합니다.",
                        },
                    },
                ],
            },
        }
        schema = '<script type="application/ld+json">' + json.dumps(schema_payload, ensure_ascii=False) + '</script>'

    if '<section class="cta">' in text and 'faq-section' not in text:
        text = text.replace('<section class="cta">', faq_html + '\n<section class="cta">', 1)
    if '</head>' in text and 'application/ld+json' not in text:
        text = text.replace('</head>', schema + '\n</head>', 1)
    if 'alt="파워잉글리쉬 수업 안내 이미지"' in text:
        text = text.replace('alt="파워잉글리쉬 수업 안내 이미지"', f'alt="{alt_text}"', 1)
    path.write_text(text, encoding='utf-8', newline='\n')

print('SEO blocks added to regional pages')
