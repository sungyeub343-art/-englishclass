from argparse import ArgumentParser
from datetime import date
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent
SITE_URL = "https://englishclass.kr"
FILENAME = "business-english-speaking-inquiry.html"
TITLE = "지역별(시군구) + 직장인 영어스피킹 문의"
EXPECTED_REGION_COUNT = 17
EXPECTED_DISTRICT_COUNT = 229


def inquiry_filename(source_filename: str) -> str:
  return source_filename.replace("english-", "business-english-speaking-", 1)


def region_map() -> list[tuple[str, str, list[tuple[str, str]]]]:
    index_text = (ROOT / "english.html").read_text(encoding="utf-8")
    regions = re.findall(
        r"class='region-card' href='(english-[^']+\.html)'><strong>([^<]+)</strong>",
        index_text,
    )
    if len(regions) != EXPECTED_REGION_COUNT:
        raise ValueError(f"Expected {EXPECTED_REGION_COUNT} regions, got {len(regions)}")

    mapping = []
    for region_filename, region_name in regions:
        region_path = ROOT / region_filename
        region_text = region_path.read_text(encoding="utf-8")
        districts = re.findall(
            r"class='chip' href='(english-[^']+\.html)'>([^<]+)</a>",
            region_text,
        )
        if not districts:
            raise ValueError(f"No districts found in {region_filename}")
        if len(districts) != len({filename for filename, _ in districts}):
            raise ValueError(f"Duplicate district links in {region_filename}")
        if not all((ROOT / filename).exists() for filename, _ in districts):
            raise ValueError(f"Broken district link in {region_filename}")
        mapping.append((region_name, region_filename, districts))

    district_count = sum(len(districts) for _, _, districts in mapping)
    if district_count != EXPECTED_DISTRICT_COUNT:
        raise ValueError(f"Expected {EXPECTED_DISTRICT_COUNT} districts, got {district_count}")
    return mapping


def render_page(mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> str:
    sections = []
    for region_name, region_filename, districts in mapping:
        links = "\n".join(
        f'          <a href="{inquiry_filename(filename)}">{escape(district_name)} 직장인 영어스피킹 문의</a>'
            for filename, district_name in districts
        )
        sections.append(
            f'''      <section class="region-group" data-region="{escape(region_name)}">
        <div class="region-heading">
          <h2>{escape(region_name)}</h2>
          <a href="{region_filename}">{escape(region_name)} 전체 보기</a>
        </div>
        <div class="district-grid">
{links}
        </div>
      </section>'''
        )
    region_sections = "\n".join(sections)

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="전국 229개 시·군·구별 직장인 영어스피킹 상담 페이지를 찾아보고 1:1 화상 영어회화 무료 레벨테스트를 신청하세요.">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/{FILENAME}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="전국 시·군·구를 선택해 직장인 영어스피킹 맞춤 상담과 무료 레벨테스트를 시작하세요.">
<meta property="og:url" content="{SITE_URL}/{FILENAME}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="전국 시·군·구별 직장인 영어스피킹 문의 페이지입니다.">
<meta name="twitter:image" content="{SITE_URL}/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f5f4ef;--ink:#16213b;--muted:#59637b;--line:#ddd8cb;--accent:#f0523b;--accent-dark:#bd3429;--paper:#fff;--maxw:1180px}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;font-family:'Noto Sans KR',sans-serif;color:var(--ink);background:linear-gradient(180deg,#f5f4ef 0,#eef3f2 46%,#f7f6f2 100%)}}
a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 40px,var(--maxw));margin:0 auto}}
header{{position:sticky;top:0;z-index:10;border-bottom:1px solid var(--line);background:rgba(245,244,239,.94);backdrop-filter:blur(8px)}}
.nav{{min-height:68px;display:flex;align-items:center;justify-content:space-between;gap:20px}}
.logo{{font:700 27px/1 'Fraunces',serif}}.logo span{{color:var(--accent)}}
.nav-links{{display:flex;align-items:center;gap:18px;font-size:14px;font-weight:700;color:var(--muted)}}
.nav-links .apply{{padding:10px 15px;background:var(--ink);color:#fff;border-radius:6px}}
.hero{{padding:66px 0 38px}}
.eyebrow{{margin:0 0 13px;color:var(--accent-dark);font-weight:800}}
h1{{max-width:900px;margin:0;font:700 clamp(36px,6vw,66px)/1.13 'Fraunces','Noto Sans KR',serif;letter-spacing:0}}
.lead{{max-width:760px;margin:20px 0 0;color:var(--muted);font-size:18px;line-height:1.75}}
.hero-actions{{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}}
.button{{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 18px;border-radius:6px;font-weight:800}}
.button.primary{{background:var(--accent);color:#fff}}.button.secondary{{border:1px solid var(--line);background:#fff}}
.brand-visual{{margin:8px 0 42px}}
.brand-visual img{{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px}}
.finder{{padding:30px 0 74px}}
.finder-head{{display:grid;grid-template-columns:1fr minmax(280px,420px);gap:28px;align-items:end;margin-bottom:30px}}
.finder h2{{margin:0;font-size:30px}}.finder-head p{{margin:8px 0 0;color:var(--muted);line-height:1.7}}
.search-label{{display:block;margin-bottom:8px;font-size:13px;font-weight:800;color:var(--muted)}}
#district-search{{width:100%;height:48px;padding:0 14px;border:1px solid #bfc7cf;border-radius:6px;background:#fff;color:var(--ink);font:500 16px 'Noto Sans KR',sans-serif}}
#district-search:focus{{outline:3px solid rgba(240,82,59,.2);border-color:var(--accent)}}
.region-group{{padding:26px 0;border-top:1px solid var(--line)}}
.region-heading{{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:15px}}
.region-heading h2{{margin:0;font-size:24px}}.region-heading a{{color:var(--accent-dark);font-size:14px;font-weight:800}}
.district-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}}
.district-grid a{{display:flex;align-items:center;min-height:46px;padding:10px 12px;border:1px solid var(--line);border-radius:6px;background:var(--paper);font-size:14px;font-weight:700;line-height:1.45}}
.district-grid a:hover{{border-color:var(--accent);color:var(--accent-dark)}}
.no-results{{display:none;padding:30px 0;border-top:1px solid var(--line);color:var(--muted);font-weight:700}}
.closing{{padding:52px 0;background:var(--ink);color:#fff}}
.closing-inner{{display:flex;align-items:center;justify-content:space-between;gap:24px}}
.closing h2{{margin:0 0 8px;font-size:28px}}.closing p{{margin:0;color:#ccd3e0;line-height:1.7}}
.closing .button{{flex:0 0 auto;background:#fff;color:var(--ink)}}
footer{{padding:30px 0;color:#737c90;font-size:13px}}
@media (max-width:900px){{.district-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.finder-head{{grid-template-columns:1fr}}}}
@media (max-width:560px){{.wrap{{width:min(100% - 28px,var(--maxw))}}.nav{{align-items:flex-start;padding:16px 0}}.nav-links{{gap:10px;flex-wrap:wrap;justify-content:flex-end}}.nav-links a:first-child{{display:none}}.hero{{padding-top:48px}}.lead{{font-size:16px}}.district-grid{{grid-template-columns:1fr}}.closing-inner{{align-items:flex-start;flex-direction:column}}}}
</style>
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="logo" href="index.html"><span>파워</span>잉글리쉬</a>
    <nav class="nav-links" aria-label="주요 메뉴">
      <a href="english.html">영어회화 지역 보기</a>
      <a class="apply" href="index.html#apply">무료 레벨테스트</a>
    </nav>
  </div>
</header>
<main>
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">전국 229개 시·군·구 맞춤 상담</p>
      <h1>{TITLE}</h1>
      <p class="lead">근무 지역이나 거주 지역을 선택하면 직장인 영어스피킹 상담 페이지로 이동합니다. 업무 회화, 영어 면접, 회의와 발표 등 필요한 상황을 무료 레벨테스트에서 알려주세요.</p>
      <div class="hero-actions">
        <a class="button primary" href="#regions">지역 선택하기</a>
        <a class="button secondary" href="index.html#apply">바로 문의하기</a>
      </div>
    </div>
  </section>
  <div class="wrap brand-visual">
    <img src="og-image.png" alt="파워잉글리쉬 영어 중국어 일본어 1대1 화상회화 안내" width="1200" height="630">
  </div>
  <section class="finder" id="regions">
    <div class="wrap">
      <div class="finder-head">
        <div>
          <h2>시·군·구별 직장인 영어스피킹</h2>
          <p>전국 지역을 한곳에 모았습니다. 원하는 시·군·구를 선택해 상세 수업 안내를 확인하세요.</p>
        </div>
        <div>
          <label class="search-label" for="district-search">시·군·구 찾기</label>
          <input id="district-search" type="search" placeholder="예: 종로구, 수원시, 해운대구" autocomplete="off">
        </div>
      </div>
{region_sections}
      <p class="no-results" role="status">일치하는 지역이 없습니다. 시·군·구 이름을 다시 확인해 주세요.</p>
    </div>
  </section>
  <section class="closing">
    <div class="wrap closing-inner">
      <div><h2>직장인 영어스피킹, 현재 수준부터 확인하세요</h2><p>가능한 시간대와 업무 목표를 바탕으로 1:1 화상 영어회화 수업을 안내합니다.</p></div>
      <a class="button" href="index.html#apply">무료 레벨테스트 신청</a>
    </div>
  </section>
</main>
<footer><div class="wrap">© 2026 파워잉글리쉬 · 지역별 직장인 영어스피킹 문의</div></footer>
<script>
const search = document.querySelector('#district-search');
const groups = [...document.querySelectorAll('.region-group')];
const noResults = document.querySelector('.no-results');
search.addEventListener('input', () => {{
  const query = search.value.trim().replace(/\\s/g, '').toLowerCase();
  let visibleCount = 0;
  groups.forEach((group) => {{
    const links = [...group.querySelectorAll('.district-grid a')];
    let groupCount = 0;
    links.forEach((link) => {{
      const visible = !query || link.textContent.replace(/\\s/g, '').toLowerCase().includes(query);
      link.hidden = !visible;
      if (visible) groupCount += 1;
    }});
    group.hidden = groupCount === 0;
    visibleCount += groupCount;
  }});
  noResults.style.display = visibleCount ? 'none' : 'block';
}});
</script>
</body>
</html>
'''


def render_district_page(
    region_name: str,
    region_filename: str,
    district_name: str,
    source_filename: str,
    variant: int,
) -> str:
    location = f"{region_name} {district_name}"
    filename = inquiry_filename(source_filename)
    title = f"{location} 직장인 영어스피킹 문의"
    focus_sets = (
        ("회의와 보고", "회의에서 의견을 제시하고 진행 상황을 간결하게 보고하는 표현", "업무 핵심을 먼저 말하고 근거와 다음 행동을 덧붙이는 순서로 답변을 연습합니다."),
        ("영어 면접과 자기소개", "경력, 담당 업무, 성과를 자연스럽게 설명하는 표현", "짧은 자기소개부터 예상 질문과 후속 질문까지 실제 면접 흐름으로 연습합니다."),
        ("전화와 온라인 미팅", "연결 확인, 일정 조율, 요청 사항을 정확히 전달하는 표현", "상대의 말을 다시 확인하고 핵심 내용을 정리하는 실무 대화 습관을 만듭니다."),
        ("발표와 비즈니스 미팅", "자료를 설명하고 질문에 응답하며 의견 차이를 조율하는 표현", "발표 도입, 핵심 설명, 질의응답을 단계별로 나누어 반복 훈련합니다."),
    )
    focus, skill, method = focus_sets[variant % len(focus_sets)]
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{location} 직장인을 위한 1:1 영어스피킹 상담 페이지입니다. {focus}, 실무 대화 목표에 맞춘 수업과 무료 레벨테스트를 안내합니다.">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/{filename}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="article">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{location} 직장인 영어스피킹 목표와 일정에 맞는 1:1 화상 수업을 상담하세요.">
<meta property="og:url" content="{SITE_URL}/{filename}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{location} 직장인을 위한 맞춤 영어스피킹 상담과 무료 레벨테스트 안내입니다.">
<meta name="twitter:image" content="{SITE_URL}/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f6f4ee;--ink:#18223a;--muted:#5d6578;--line:#ddd8ca;--accent:#ed543f;--accent-dark:#b8352b;--paper:#fff;--maxw:1040px}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:'Noto Sans KR',sans-serif;color:var(--ink);background:linear-gradient(160deg,#f6f4ee 0,#edf3f0 56%,#f8f7f3 100%)}}
a{{color:inherit;text-decoration:none}}.wrap{{width:min(100% - 40px,var(--maxw));margin:0 auto}}
header{{border-bottom:1px solid var(--line);background:rgba(246,244,238,.94)}}
.nav{{min-height:68px;display:flex;align-items:center;justify-content:space-between;gap:18px}}
.logo{{font:700 27px/1 'Fraunces',serif}}.logo span{{color:var(--accent)}}
.back{{color:var(--muted);font-size:14px;font-weight:700}}
.breadcrumb{{display:flex;flex-wrap:wrap;gap:7px;padding:16px 0 0;color:var(--muted);font-size:13px}}
.hero{{padding:50px 0 36px}}.eyebrow{{margin:0 0 12px;color:var(--accent-dark);font-weight:800}}
h1{{max-width:850px;margin:0;font:700 clamp(34px,6vw,58px)/1.13 'Fraunces','Noto Sans KR',serif;letter-spacing:0}}
.lead{{max-width:760px;margin:18px 0 0;color:var(--muted);font-size:17px;line-height:1.8}}
.hero-actions{{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}}
.button{{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 18px;border-radius:6px;font-weight:800}}
.button.primary{{background:var(--accent);color:#fff}}.button.ghost{{border:1px solid var(--line);background:#fff}}
.visual{{padding:0 0 42px}}.visual img{{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px}}
.summary{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;padding:0 0 44px}}
.summary article{{padding:20px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}}
.summary h2{{margin:0 0 9px;font-size:18px}}.summary p{{margin:0;color:var(--muted);font-size:14px;line-height:1.7}}
.content{{padding:2px 0 56px}}.content-grid{{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(260px,.65fr);gap:18px}}
.panel{{padding:26px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}}
.panel h2{{margin:0 0 14px;font-size:25px;line-height:1.4}}.panel h3{{margin:24px 0 8px;font-size:18px}}
.panel p{{margin:0 0 13px;color:var(--muted);line-height:1.85}}.panel ul{{margin:0;padding-left:20px;color:var(--muted)}}.panel li{{margin:0 0 12px;line-height:1.75}}
.label{{display:inline-block;margin-bottom:14px;padding:7px 10px;background:#fff1ed;color:var(--accent-dark);font-size:13px;font-weight:800}}
.cta{{padding:46px 0;background:var(--ink);color:#fff}}.cta-inner{{display:flex;align-items:center;justify-content:space-between;gap:22px}}
.cta h2{{margin:0 0 7px;font-size:27px}}.cta p{{margin:0;color:#cdd3df;line-height:1.7}}.cta .button{{flex:0 0 auto;background:#fff;color:var(--ink)}}
footer{{padding:30px 0;color:#747d90;font-size:13px}}
@media (max-width:780px){{.summary,.content-grid{{grid-template-columns:1fr}}.cta-inner{{align-items:flex-start;flex-direction:column}}}}
@media (max-width:520px){{.wrap{{width:min(100% - 28px,var(--maxw))}}.nav{{align-items:flex-start;padding:16px 0}}.back{{max-width:150px;text-align:right}}.hero{{padding-top:40px}}.lead{{font-size:15px}}.panel{{padding:20px}}}}
</style>
</head>
<body>
<header><div class="wrap nav"><a class="logo" href="index.html"><span>파워</span>잉글리쉬</a><a class="back" href="{FILENAME}">전국 직장인 영어스피킹 지역 보기</a></div></header>
<main>
  <div class="wrap breadcrumb" aria-label="빵부스러기"><a href="index.html">홈</a><span>›</span><a href="{FILENAME}">직장인 영어스피킹</a><span>›</span><a href="{region_filename}">{region_name}</a><span>›</span><span>{district_name}</span></div>
  <section class="hero"><div class="wrap">
    <p class="eyebrow">{location} · 1:1 화상 영어회화</p>
    <h1>{title}</h1>
    <p class="lead">업무 중 영어로 말해야 하는 순간에 대비할 수 있도록 현재 스피킹 수준과 필요한 상황을 먼저 확인합니다. {location} 직장인의 일정과 목표에 맞춰 실무 중심 수업 방향을 안내합니다.</p>
    <div class="hero-actions"><a class="button primary" href="index.html#apply">무료 레벨테스트 신청</a><a class="button ghost" href="{source_filename}">{location} 영어회화 보기</a></div>
  </div></section>
  <section class="visual"><div class="wrap"><img src="og-image.png" alt="파워잉글리쉬 1대1 화상 영어스피킹 안내" width="1200" height="630"></div></section>
  <section><div class="wrap summary">
    <article><h2>업무 상황 진단</h2><p>회의, 면접, 발표, 전화 중 영어가 가장 필요한 장면과 현재 어려움을 구체적으로 확인합니다.</p></article>
    <article><h2>직장인 일정 반영</h2><p>출근 전, 퇴근 후, 주말 등 가능한 시간대를 기준으로 꾸준히 이어갈 수 있는 수업을 안내합니다.</p></article>
    <article><h2>1:1 발화 연습</h2><p>설명만 듣기보다 직접 말하고 즉시 교정받으며 실무 표현을 자신의 문장으로 익힙니다.</p></article>
  </div></section>
  <section class="content"><div class="wrap content-grid">
    <article class="panel">
      <span class="label">{focus} 중심 상담</span>
      <h2>{location} 직장인 영어스피킹, 실제 업무에 필요한 말하기부터 준비합니다</h2>
      <p>{location}에서 직장인 영어스피킹 수업을 찾을 때는 막연한 프리토킹보다 영어를 쓰게 되는 업무 장면을 먼저 정하는 편이 효과적입니다. 상담에서는 담당 업무, 영어 사용 빈도, 원하는 수업 시간과 목표 기간을 확인한 뒤 학습 우선순위를 함께 정합니다.</p>
      <p>이번 수업 방향은 {skill}을 중심으로 구성할 수 있습니다. 알고 있는 표현도 실제 대화에서는 바로 나오지 않을 수 있으므로 짧게 대답하기, 이유 덧붙이기, 상대에게 다시 질문하기를 연결해 말하는 시간을 늘립니다.</p>
      <h3>업무 표현을 내 문장으로 바꾸는 연습</h3>
      <p>{method} 수업 중 자주 막힌 문장과 교정받은 표현은 다음 시간에 다시 사용해 단순 암기가 실제 발화로 이어지도록 합니다.</p>
      <h3>레벨에 맞춘 1:1 진행</h3>
      <p>기초 단계는 짧고 정확한 문장과 필수 질문 패턴부터 시작하고, 중급 이상은 의견 설명, 반론 대응, 조건 협의처럼 더 긴 대화 흐름을 다룹니다. 1:1 수업이라 학습자의 속도와 업무 분야에 맞춰 난이도를 조절할 수 있습니다.</p>
      <h3>바쁜 직장인을 위한 복습 방식</h3>
      <p>긴 과제보다 수업에서 사용한 핵심 표현을 출퇴근 시간에 소리 내어 반복하고, 다음 수업에서 같은 상황을 다시 말해 보는 방식이 효율적입니다. 꾸준히 참여할 수 있는 횟수와 시간대를 정하는 것도 상담에 포함됩니다.</p>
    </article>
    <aside class="panel">
      <h2>상담 전에 알려주세요</h2>
      <ul>
        <li>영어를 가장 자주 사용하는 업무 상황</li>
        <li>회의, 발표, 면접 등 우선 준비할 목표</li>
        <li>현재 말하기 수준과 어려운 부분</li>
        <li>가능한 요일과 수업 시간대</li>
        <li>목표 일정 또는 준비 기간</li>
      </ul>
    </aside>
  </div></section>
  <section class="cta"><div class="wrap cta-inner"><div><h2>{location} 직장인 영어스피킹 상담</h2><p>무료 레벨테스트로 현재 수준을 확인하고 필요한 업무 영어부터 시작하세요.</p></div><a class="button" href="index.html#apply">무료 상담 신청</a></div></section>
</main>
<footer><div class="wrap">© 2026 파워잉글리쉬 · {location} 직장인 영어스피킹 문의</div></footer>
</body>
</html>
'''


def update_sitemap(detail_filenames: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    url_pattern = rf"{re.escape(SITE_URL)}/(?:{re.escape(FILENAME)}|business-english-speaking-[^<]+\.html)"
    text = re.sub(
        rf"\s*<url>\s*<loc>{url_pattern}</loc>.*?</url>",
        "",
        text,
        flags=re.S,
    )
    urls = [FILENAME, *detail_filenames]
    entries = "".join(f'''  <url>
    <loc>{SITE_URL}/{filename}</loc>
    <lastmod>{date.today().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"0.9" if filename == FILENAME else "0.7"}</priority>
  </url>
''' for filename in urls)
    text = text.replace("</urlset>", entries + "</urlset>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate(mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> None:
    path = ROOT / FILENAME
    text = path.read_text(encoding="utf-8")
    expected_links = {
      inquiry_filename(filename)
        for _, _, districts in mapping
        for filename, _ in districts
    }
    actual_links = set(re.findall(r'<a href="(business-english-speaking-[^"]+\.html)">[^<]+ 직장인 영어스피킹 문의</a>', text))
    if actual_links != expected_links:
        raise ValueError("Missing or unexpected district links")
    if f"<title>{TITLE}</title>" not in text or f"<h1>{TITLE}</h1>" not in text:
        raise ValueError("Required page title is missing")
    if f'<link rel="canonical" href="{SITE_URL}/{FILENAME}">' not in text:
        raise ValueError("Invalid canonical URL")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    if urls.count(f"{SITE_URL}/{FILENAME}") != 1:
        raise ValueError("Invalid sitemap entry")
    expected_urls = {f"{SITE_URL}/{filename}" for filename in expected_links}
    actual_urls = {
      url
      for url in urls
      if url and "/business-english-speaking-" in url and url != f"{SITE_URL}/{FILENAME}"
    }
    if actual_urls != expected_urls:
      raise ValueError("Invalid district sitemap entries")

    for region_name, _, districts in mapping:
      for source_filename, district_name in districts:
        filename = inquiry_filename(source_filename)
        detail_text = (ROOT / filename).read_text(encoding="utf-8")
        title = f"{region_name} {district_name} 직장인 영어스피킹 문의"
        if f"<title>{title}</title>" not in detail_text or f"<h1>{title}</h1>" not in detail_text:
          raise ValueError(f"Invalid title in {filename}")
        if f'<link rel="canonical" href="{SITE_URL}/{filename}">' not in detail_text:
          raise ValueError(f"Invalid canonical URL in {filename}")
        if f'href="{source_filename}"' not in detail_text:
          raise ValueError(f"Missing source page link in {filename}")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate region sources without writing files")
    parser.add_argument("--validate", action="store_true", help="Validate generated output without writing files")
    args = parser.parse_args()

    mapping = region_map()
    if args.check:
        print(f"Matched {len(mapping)} regions and {sum(len(districts) for _, _, districts in mapping)} districts")
        return
    if args.validate:
        validate(mapping)
        print(f"Validated {FILENAME} with {EXPECTED_DISTRICT_COUNT} district links")
        return

    (ROOT / FILENAME).write_text(render_page(mapping), encoding="utf-8", newline="\n")
    detail_filenames = []
    page_index = 0
    for region_name, region_filename, districts in mapping:
      for source_filename, district_name in districts:
        filename = inquiry_filename(source_filename)
        detail_filenames.append(filename)
        (ROOT / filename).write_text(
          render_district_page(
            region_name,
            region_filename,
            district_name,
            source_filename,
            page_index,
          ),
          encoding="utf-8",
          newline="\n",
        )
        page_index += 1
    update_sitemap(detail_filenames)
    validate(mapping)
    print(f"Generated {FILENAME} and {len(detail_filenames)} district inquiry pages")
    print("Updated and validated sitemap.xml")


if __name__ == "__main__":
    main()