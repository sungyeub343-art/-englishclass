from pathlib import Path
import re


ROOT = Path(r"c:\Users\M\Desktop\회화")


DETAIL_CSS = """.detail{padding:0 0 34px}
.detail-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:18px}
.detail-box{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px}
.detail-box h2{margin:0 0 14px;font-size:24px;line-height:1.3}
.detail-box h3{margin:20px 0 8px;font-size:18px}
.detail-box p{margin:0 0 12px;color:var(--muted);font-size:15px;line-height:1.8}
.detail-box ul{margin:0;padding-left:18px;color:var(--muted)}
.detail-box li{margin:0 0 10px;line-height:1.7}
.tag-list{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:14px}
.tag-list span{display:inline-flex;align-items:center;padding:8px 12px;border:1px solid var(--line);border-radius:999px;background:#fff7f1;color:#7a4b2b;font-size:13px;font-weight:700}
"""


DETAIL_TEMPLATE = """<section class="detail">
  <div class="wrap detail-grid">
    <article class="detail-box">
      <div class="tag-list">
        <span>{prefix} 일본어회화</span>
        <span>직장인 일본어회화</span>
        <span>왕초보 일본어회화</span>
        <span>1:1 화상 일본어회화</span>
      </div>
      <h2>{prefix} 일본어회화, 1:1 화상 일본어회화로 목적별 맞춤 수업을 안내합니다</h2>
      <p>{prefix} 일본어회화 수업을 찾는 학습자들은 일본어 말하기, 일본어 스피킹, 여행회화, 실무 일본어회화처럼 목표가 분명한 경우가 많습니다. 파워잉글리쉬는 {prefix} 일본어회화 상담 단계에서 현재 회화 실력과 학습 목적을 먼저 확인하고, 1:1 화상 일본어회화 방식으로 발화량과 복습 효율을 함께 높일 수 있는 수업 구성을 안내합니다.</p>
      <p>특히 {prefix} 일본어회화는 왕초보 일본어회화부터 직장인 일본어회화, 일본어 발음 교정, JLPT 회화 대비까지 수요가 넓게 나뉘기 때문에 같은 커리큘럼으로 접근하면 효율이 떨어질 수 있습니다. 무료 레벨테스트 후 발음, 문장 구성, 응답 속도, 자주 막히는 표현을 점검한 뒤 일상 일본어회화, 여행 일본어회화, 실전 대화, 시험 대비 일본어회화 중 어떤 영역을 우선 강화할지 정하는 방식이 더 효과적입니다.</p>

      <h3>일상회화와 왕초보 일본어회화 중심 수업</h3>
      <p>{prefix} 일본어회화 수업 중에서도 왕초보 일본어회화는 자기소개, 일상 질문, 취미, 일정, 감정 표현처럼 반복 사용 빈도가 높은 주제로 시작하는 것이 좋습니다. 왕초보 일본어회화 단계에서는 어려운 문법 설명보다 짧은 문장을 직접 말해보는 훈련이 중요하며, 화상 일본어회화 수업에서는 발화량을 늘려 실제 일본어회화 적응 속도를 높일 수 있습니다.</p>

      <h3>여행회화와 실전 일본어 스피킹 훈련</h3>
      <p>여행회화가 목표인 경우 {prefix} 일본어회화 수업에서도 공항, 호텔, 식당, 쇼핑, 길 안내, 돌발 상황 대응처럼 실전 장면을 기준으로 연습하는 편이 효율적입니다. 여행 일본어회화는 단어 암기보다 질문 패턴과 응답 패턴을 익히는 것이 중요해서, 1:1 화상 일본어회화 방식으로 상황별 회화 흐름을 반복하면 실제 여행에서 바로 쓰기 쉬운 일본어 말하기 표현을 빠르게 정리할 수 있습니다.</p>

      <h3>비즈니스 일본어회화와 JLPT 회화 대비</h3>
      <p>시험 대비 일본어회화는 JLPT 회화, 일본어 면접, 발표 준비처럼 답변 구조와 말하기 속도가 중요한 평가에 맞춰 준비해야 합니다. 반면 직장인 일본어회화와 실무 대화는 회의, 보고, 전화 응대, 자기소개, 비즈니스 미팅처럼 실제 업무에 자주 나오는 표현을 중심으로 구성하는 것이 좋습니다. {prefix} 일본어회화 상담에서는 이 두 방향을 구분해 시험 점수 향상이 목표인지, 실무 일본어회화 활용이 목표인지에 따라 맞춤 수업을 제안할 수 있습니다.</p>
    </article>
    <aside class="detail-box">
      <h2>{prefix} 일본어회화 상담 전 참고사항</h2>
      <ul>
        <li>{prefix} 일본어회화 상담 시에는 일상회화, 여행회화, 시험 대비 일본어회화, 직장인 일본어회화 중 우선순위를 먼저 정하는 것이 중요합니다.</li>
        <li>왕초보 일본어회화는 기초 문장 반복, 발화량 확보, 스피킹 자신감 형성이 핵심이라서 수업 난이도 조절이 특히 중요합니다.</li>
        <li>직장인 일본어회화는 저녁 시간대, 주말 수업, 과제 분량, 복습 방식까지 함께 정해야 실제 수업 지속률이 높아집니다.</li>
        <li>시험 대비 일본어회화는 JLPT 회화, 일본어 면접, 발표 준비처럼 목표 상황을 구체적으로 정할수록 준비 방향이 명확해집니다.</li>
        <li>1:1 화상 일본어회화는 이동 시간 없이 꾸준히 참여하기 쉬워 {prefix} 직장인, 초보 학습자, 일정이 불규칙한 수강생에게 적합합니다.</li>
      </ul>
    </aside>
  </div>
</section>
"""


TITLE_RE = re.compile(r"<title>(?P<prefix>.+?) 일본어회화 1:1 화상회화 무료상담 \| 파워잉글리쉬</title>")
DESCRIPTION_RE = re.compile(r'<meta name="description" content=".+?">')
OG_TITLE_RE = re.compile(r'<meta property="og:title" content=".+?">')
OG_DESCRIPTION_RE = re.compile(r'<meta property="og:description" content=".+?">')
CSS_RE = re.compile(r'\.card p\{margin:0;color:var\(--muted\);font-size:14\.5px;line-height:1\.65\}')
CTA_RE = re.compile(r'<section class="cta">\s*<div class="wrap">\s*<div class="cta-box">\s*<p>.*?</p>', re.S)
MOBILE_MEDIA_RE = re.compile(r'@media \(max-width:840px\)\{\.cards\{grid-template-columns:1fr\}\.hero p\{font-size:15px\}\}')


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "detail-grid" in text or "tag-list" in text:
        return False

    match = TITLE_RE.search(text)
    if not match:
        return False

    prefix = match.group("prefix")

    text = TITLE_RE.sub(
        rf'<title>{prefix} 일본어회화 1:1 화상 스피킹 수업 | 무료 레벨테스트 | 파워잉글리쉬</title>',
        text,
        count=1,
    )
    text = DESCRIPTION_RE.sub(
        rf'<meta name="description" content="{prefix} 일본어회화, 일본어 스피킹, 발음 교정, 여행회화까지 1:1 화상 수업으로 맞춤 상담을 제공합니다.">',
        text,
        count=1,
    )
    text = OG_TITLE_RE.sub(
        rf'<meta property="og:title" content="{prefix} 일본어회화 1:1 화상 스피킹 수업">',
        text,
        count=1,
    )
    text = OG_DESCRIPTION_RE.sub(
        rf'<meta property="og:description" content="{prefix} 지역 학습자에게 맞춘 일본어회화, 발음 교정, 여행회화, 무료 레벨테스트 상담 페이지입니다.">',
        text,
        count=1,
    )

    text = CSS_RE.sub(
        r'.card p{margin:0;color:var(--muted);font-size:14.5px;line-height:1.65}\n' + DETAIL_CSS.rstrip(),
        text,
        count=1,
    )

    text = text.replace(
        '</section>\n<section class="cta">',
        '</section>\n' + DETAIL_TEMPLATE.format(prefix=prefix) + '\n<section class="cta">',
        1,
    )

    text = CTA_RE.sub(
        rf'<section class="cta">\n  <div class="wrap">\n    <div class="cta-box">\n      <p>{prefix} 일본어회화 상담은 무료 레벨테스트 신청으로 바로 시작할 수 있습니다. 일본어 스피킹, 발음 교정, 여행회화, 성인 맞춤 수업까지 목적에 맞게 안내합니다.</p>',
        text,
        count=1,
    )

    text = MOBILE_MEDIA_RE.sub(
        '@media (max-width:840px){.cards{grid-template-columns:1fr}.detail-grid{grid-template-columns:1fr}.hero p{font-size:15px}}',
        text,
        count=1,
    )

    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    updated = 0
    skipped = 0
    for path in ROOT.glob("japanese-*-*.html"):
        if update_file(path):
            updated += 1
        else:
            skipped += 1
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    main()