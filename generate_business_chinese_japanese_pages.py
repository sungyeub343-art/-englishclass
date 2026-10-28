from argparse import ArgumentParser
from datetime import date
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent
SITE_URL = "https://englishclass.kr"
EXPECTED_REGION_COUNT = 17
EXPECTED_DISTRICT_COUNT = 229

LANGUAGES = {
    "chinese": {
        "name": "중국어",
        "hub_label": "중국어회화",
        "prefix": "business-chinese",
        "image": "[복사본] 파워CH 중국어.jpg",
        "image_size": (1080, 10800),
        "situations": "중국 거래처 미팅, 출장, 전화와 위챗 업무 소통",
        "focus_sets": (
            ("거래처 미팅과 상담", "제품과 조건을 설명하고 상대의 요청을 확인하는 중국어 표현", "인사와 소개, 핵심 제안, 질문 확인을 한 흐름으로 묶어 실제 미팅처럼 연습합니다."),
            ("중국 출장과 현장 소통", "공항, 호텔, 공장 방문, 식사 자리에서 필요한 실무 중국어 표현", "출장 일정 순서대로 상황을 나누어 짧은 문장부터 대화를 이어가는 연습을 합니다."),
            ("전화와 메신저 업무", "일정 조율, 납기 확인, 요청 사항을 정확히 전달하는 중국어 표현", "숫자, 날짜, 수량을 다시 확인하는 습관을 만들고 핵심 내용을 정리해 말하는 연습을 합니다."),
            ("가격 협상과 계약 조건", "단가, 수량, 결제 조건을 제시하고 조율하는 중국어 표현", "제안, 반대 의견, 대안 제시를 단계별로 나누어 협상 대화를 반복 훈련합니다."),
        ),
        "pronunciation": "성조와 발음은 업무 대화에서 의미 전달에 직접 영향을 주기 때문에, 자주 쓰는 업무 어휘의 성조를 문장 단위로 교정합니다.",
        "checklist": (
            "중국어를 사용하는 업무 상황과 상대(거래처, 공장, 동료 등)",
            "미팅, 출장, 전화, 협상 등 우선 준비할 목표",
            "현재 중국어 수준과 HSK 등 학습 경험",
            "가능한 요일과 수업 시간대",
            "목표 일정 또는 준비 기간",
        ),
    },
    "japanese": {
        "name": "일본어",
        "hub_label": "일본어회화",
        "prefix": "business-japanese",
        "image": "[복사본] 파워JP 일본어.jpg",
        "image_size": (1080, 12960),
        "situations": "일본 거래처 미팅, 경어 응대, 전화와 이메일 업무 소통",
        "focus_sets": (
            ("경어와 비즈니스 매너", "존경어와 겸양어를 상황에 맞게 구분해 쓰는 일본어 표현", "자기소개, 명함 교환, 방문 인사처럼 정해진 장면부터 경어를 자연스럽게 말하는 연습을 합니다."),
            ("거래처 미팅과 회의", "의견을 정중하게 제시하고 상대의 의도를 확인하는 일본어 표현", "결론을 부드럽게 전달하고 확인 질문을 덧붙이는 일본식 회의 흐름으로 연습합니다."),
            ("전화 응대와 일정 조율", "전화 받기, 담당자 연결, 약속 변경을 정확히 전달하는 일본어 표현", "자주 쓰는 전화 응대 문형을 익힌 뒤 예상하지 못한 질문에 대응하는 롤플레이를 반복합니다."),
            ("일본 출장과 접대", "방문, 식사 자리, 현장 견학에서 필요한 실무 일본어 표현", "출장 일정 순서대로 장면을 나누어 인사부터 감사 표현까지 이어서 말하는 연습을 합니다."),
        ),
        "pronunciation": "일본어는 문장 끝 표현과 경어 수준에 따라 인상이 크게 달라지기 때문에, 같은 내용을 상대와 상황에 맞는 말투로 바꿔 말하는 연습을 함께 합니다.",
        "checklist": (
            "일본어를 사용하는 업무 상황과 상대(거래처, 본사, 동료 등)",
            "미팅, 전화 응대, 출장, 이메일 등 우선 준비할 목표",
            "현재 일본어 수준과 JLPT 등 학습 경험",
            "가능한 요일과 수업 시간대",
            "목표 일정 또는 준비 기간",
        ),
    },
}


BUSINESS_INQUIRY_CSS = """.business-inquiry{display:flex;align-items:center;justify-content:space-between;gap:20px;margin:0 0 24px;padding:20px;border:1px solid var(--line);border-left:5px solid var(--a);border-radius:8px;background:#fff}
.business-inquiry strong{display:block;font-size:19px}.business-inquiry span{display:block;margin-top:5px;color:var(--muted);line-height:1.6}
.business-inquiry b{flex:0 0 auto;color:var(--a);font-size:14px}
"""


def hub_filename(lang: str) -> str:
    return f"{LANGUAGES[lang]['prefix']}-inquiry.html"


def detail_filename(lang: str, source_filename: str) -> str:
    return source_filename.replace(f"{lang}-", f"{LANGUAGES[lang]['prefix']}-", 1)


def region_map(lang: str) -> list[tuple[str, str, list[tuple[str, str]]]]:
    index_text = (ROOT / f"{lang}.html").read_text(encoding="utf-8")
    regions = re.findall(
        rf"class='region-card' href='({lang}-[^']+\.html)'><strong>([^<]+)</strong>",
        index_text,
    )
    if len(regions) != EXPECTED_REGION_COUNT:
        raise ValueError(f"Expected {EXPECTED_REGION_COUNT} {lang} regions, got {len(regions)}")

    mapping = []
    for region_filename, region_name in regions:
        region_text = (ROOT / region_filename).read_text(encoding="utf-8")
        districts = re.findall(
            rf"class='chip' href='({lang}-[^']+\.html)'>([^<]+)</a>",
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
        raise ValueError(f"Expected {EXPECTED_DISTRICT_COUNT} {lang} districts, got {district_count}")
    return mapping


def render_hub_page(lang: str, mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> str:
    info = LANGUAGES[lang]
    name = info["name"]
    filename = hub_filename(lang)
    title = f"지역별(시군구) + 비즈니스 {name} 문의"
    sections = []
    for region_name, region_filename, districts in mapping:
        links = "\n".join(
            f'          <a href="{detail_filename(lang, district_file)}">{escape(district_name)} 비즈니스 {name} 문의</a>'
            for district_file, district_name in districts
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
<title>{title}</title>
<meta name="description" content="전국 229개 시·군·구별 비즈니스 {name} 상담 페이지를 찾아보고 1:1 화상 {name}회화 무료 레벨테스트를 신청하세요.">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/{filename}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="전국 시·군·구를 선택해 비즈니스 {name} 맞춤 상담과 무료 레벨테스트를 시작하세요.">
<meta property="og:url" content="{SITE_URL}/{filename}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="전국 시·군·구별 비즈니스 {name} 문의 페이지입니다.">
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
      <a href="{lang}.html">{info["hub_label"]} 지역 보기</a>
      <a class="apply" href="index.html#apply">무료 레벨테스트</a>
    </nav>
  </div>
</header>
<main>
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">전국 229개 시·군·구 맞춤 상담</p>
      <h1>{title}</h1>
      <p class="lead">근무 지역이나 거주 지역을 선택하면 비즈니스 {name} 상담 페이지로 이동합니다. {info["situations"]} 등 필요한 상황을 무료 레벨테스트에서 알려주세요.</p>
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
          <h2>시·군·구별 비즈니스 {name}</h2>
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
      <div><h2>비즈니스 {name}, 현재 수준부터 확인하세요</h2><p>가능한 시간대와 업무 목표를 바탕으로 1:1 화상 {name}회화 수업을 안내합니다.</p></div>
      <a class="button" href="index.html#apply">무료 레벨테스트 신청</a>
    </div>
  </section>
</main>
<footer><div class="wrap">© 2026 파워잉글리쉬 · 지역별 비즈니스 {name} 문의</div></footer>
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
    lang: str,
    region_name: str,
    region_filename: str,
    district_name: str,
    source_filename: str,
    variant: int,
) -> str:
    info = LANGUAGES[lang]
    name = info["name"]
    location = f"{region_name} {district_name}"
    filename = detail_filename(lang, source_filename)
    title = f"{location} 비즈니스 {name} 문의"
    focus, skill, method = info["focus_sets"][variant % len(info["focus_sets"])]
    image_width, image_height = info["image_size"]
    checklist = "\n".join(f"        <li>{item}</li>" for item in info["checklist"])
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{location} 직장인을 위한 1:1 비즈니스 {name} 상담 페이지입니다. {focus}, 실무 대화 목표에 맞춘 수업과 무료 레벨테스트를 안내합니다.">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/{filename}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="article">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{location} 비즈니스 {name} 목표와 일정에 맞는 1:1 화상 수업을 상담하세요.">
<meta property="og:url" content="{SITE_URL}/{filename}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{location} 직장인을 위한 맞춤 비즈니스 {name} 상담과 무료 레벨테스트 안내입니다.">
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
<header><div class="wrap nav"><a class="logo" href="index.html"><span>파워</span>잉글리쉬</a><a class="back" href="{hub_filename(lang)}">전국 비즈니스 {name} 지역 보기</a></div></header>
<main>
  <div class="wrap breadcrumb" aria-label="빵부스러기"><a href="index.html">홈</a><span>›</span><a href="{hub_filename(lang)}">비즈니스 {name}</a><span>›</span><a href="{region_filename}">{region_name}</a><span>›</span><span>{district_name}</span></div>
  <section class="hero"><div class="wrap">
    <p class="eyebrow">{location} · 1:1 화상 {name}회화</p>
    <h1>{title}</h1>
    <p class="lead">{info["situations"]}처럼 업무에서 {name}로 말해야 하는 순간에 대비할 수 있도록 현재 수준과 필요한 상황을 먼저 확인합니다. {location} 직장인의 일정과 목표에 맞춰 실무 중심 수업 방향을 안내합니다.</p>
    <div class="hero-actions"><a class="button primary" href="index.html#apply">무료 레벨테스트 신청</a><a class="button ghost" href="{source_filename}">{location} {name}회화 보기</a></div>
  </div></section>
  <section class="visual"><div class="wrap"><img src="{info["image"]}" alt="{location} 비즈니스 {name} 수업 안내 이미지" width="{image_width}" height="{image_height}" loading="lazy" decoding="async"></div></section>
  <section><div class="wrap summary">
    <article><h2>업무 상황 진단</h2><p>미팅, 전화, 출장, 협상 중 {name}가 가장 필요한 장면과 현재 어려움을 구체적으로 확인합니다.</p></article>
    <article><h2>직장인 일정 반영</h2><p>출근 전, 퇴근 후, 주말 등 가능한 시간대를 기준으로 꾸준히 이어갈 수 있는 수업을 안내합니다.</p></article>
    <article><h2>1:1 발화 연습</h2><p>설명만 듣기보다 직접 말하고 즉시 교정받으며 실무 표현을 자신의 문장으로 익힙니다.</p></article>
  </div></section>
  <section class="content"><div class="wrap content-grid">
    <article class="panel">
      <span class="label">{focus} 중심 상담</span>
      <h2>{location} 비즈니스 {name}, 실제 업무에 필요한 말하기부터 준비합니다</h2>
      <p>{location}에서 비즈니스 {name} 수업을 찾을 때는 교재 진도보다 {name}를 쓰게 되는 업무 장면을 먼저 정하는 편이 효과적입니다. 상담에서는 담당 업무, {name} 사용 빈도, 원하는 수업 시간과 목표 기간을 확인한 뒤 학습 우선순위를 함께 정합니다.</p>
      <p>이번 수업 방향은 {skill}을 중심으로 구성할 수 있습니다. 알고 있는 표현도 실제 대화에서는 바로 나오지 않을 수 있으므로 짧게 대답하기, 이유 덧붙이기, 상대에게 다시 질문하기를 연결해 말하는 시간을 늘립니다.</p>
      <h3>업무 표현을 내 문장으로 바꾸는 연습</h3>
      <p>{method} 수업 중 자주 막힌 문장과 교정받은 표현은 다음 시간에 다시 사용해 단순 암기가 실제 발화로 이어지도록 합니다.</p>
      <h3>발음과 말투까지 함께 교정</h3>
      <p>{info["pronunciation"]}</p>
      <h3>레벨에 맞춘 1:1 진행</h3>
      <p>기초 단계는 업무 인사와 필수 질문 패턴부터 시작하고, 중급 이상은 의견 설명, 조건 협의, 문제 상황 대응처럼 더 긴 대화 흐름을 다룹니다. 1:1 수업이라 학습자의 속도와 업무 분야에 맞춰 난이도를 조절할 수 있습니다.</p>
    </article>
    <aside class="panel">
      <h2>상담 전에 알려주세요</h2>
      <ul>
{checklist}
      </ul>
    </aside>
  </div></section>
  <section class="cta"><div class="wrap cta-inner"><div><h2>{location} 비즈니스 {name} 상담</h2><p>무료 레벨테스트로 현재 수준을 확인하고 필요한 업무 {name}부터 시작하세요.</p></div><a class="button" href="index.html#apply">무료 상담 신청</a></div></section>
</main>
<footer><div class="wrap">© 2026 파워잉글리쉬 · {location} 비즈니스 {name} 문의</div></footer>
</body>
</html>
'''


def add_hub_link(lang: str) -> None:
    info = LANGUAGES[lang]
    path = ROOT / f"{lang}.html"
    text = path.read_text(encoding="utf-8")
    if ".business-inquiry{" not in text:
        grid_rule = ".region-grid{display:grid;"
        mobile_rule = ".logo{font-size:22px}}"
        if grid_rule not in text or mobile_rule not in text:
            raise ValueError(f"CSS anchors not found in {lang}.html")
        text = text.replace(grid_rule, BUSINESS_INQUIRY_CSS + grid_rule, 1)
        text = text.replace(mobile_rule, ".logo{font-size:22px}.business-inquiry{align-items:flex-start;flex-direction:column}}", 1)
    if f'href="{hub_filename(lang)}"' in text:
        path.write_text(text, encoding="utf-8", newline="\n")
        return
    heading = f"    <h2>{info['hub_label']} 지역별 페이지</h2>\n"
    if heading not in text:
        raise ValueError(f"Region heading not found in {lang}.html")
    link = f'''    <a class="business-inquiry" href="{hub_filename(lang)}">
      <span><strong>지역별(시군구) + 비즈니스 {info["name"]} 문의</strong><span>전국 229개 시·군·구에서 직장인 맞춤 상담 페이지를 찾아보세요.</span></span>
      <b>지역 선택하기 →</b>
    </a>
'''
    path.write_text(text.replace(heading, heading + link, 1), encoding="utf-8", newline="\n")


def update_sitemap(lang: str, detail_filenames: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    prefix = LANGUAGES[lang]["prefix"]
    text = re.sub(
        rf"\s*<url>\s*<loc>{re.escape(SITE_URL)}/{re.escape(prefix)}-[^<]+\.html</loc>.*?</url>",
        "",
        text,
        flags=re.S,
    )
    hub = hub_filename(lang)
    entries = "".join(f'''  <url>
    <loc>{SITE_URL}/{filename}</loc>
    <lastmod>{date.today().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"0.9" if filename == hub else "0.7"}</priority>
  </url>
''' for filename in [hub, *detail_filenames])
    text = text.replace("</urlset>", entries + "</urlset>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate(lang: str, mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> None:
    name = LANGUAGES[lang]["name"]
    prefix = LANGUAGES[lang]["prefix"]
    hub = hub_filename(lang)
    text = (ROOT / hub).read_text(encoding="utf-8")
    expected_links = {
        detail_filename(lang, filename)
        for _, _, districts in mapping
        for filename, _ in districts
    }
    actual_links = set(re.findall(rf'<a href="({prefix}-[^"]+\.html)">[^<]+ 비즈니스 {name} 문의</a>', text))
    if actual_links != expected_links:
        raise ValueError(f"Missing or unexpected district links in {hub}")
    if f'href="{hub}"' not in (ROOT / f"{lang}.html").read_text(encoding="utf-8"):
        raise ValueError(f"Missing hub link in {lang}.html")

    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [node.text for node in ET.parse(ROOT / "sitemap.xml").findall(f".//{namespace}loc")]
    if urls.count(f"{SITE_URL}/{hub}") != 1:
        raise ValueError(f"Invalid sitemap entry for {hub}")
    actual_urls = {url for url in urls if url and f"/{prefix}-" in url and url != f"{SITE_URL}/{hub}"}
    if actual_urls != {f"{SITE_URL}/{filename}" for filename in expected_links}:
        raise ValueError(f"Invalid {prefix} sitemap entries")

    for region_name, _, districts in mapping:
        for source_filename, district_name in districts:
            filename = detail_filename(lang, source_filename)
            detail_text = (ROOT / filename).read_text(encoding="utf-8")
            title = f"{region_name} {district_name} 비즈니스 {name} 문의"
            if f"<title>{title}</title>" not in detail_text or f"<h1>{title}</h1>" not in detail_text:
                raise ValueError(f"Invalid title in {filename}")
            if f'<link rel="canonical" href="{SITE_URL}/{filename}">' not in detail_text:
                raise ValueError(f"Invalid canonical URL in {filename}")
            if f'href="{source_filename}"' not in detail_text:
                raise ValueError(f"Missing source page link in {filename}")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--validate", action="store_true", help="Validate generated output without writing files")
    args = parser.parse_args()

    for lang in LANGUAGES:
        mapping = region_map(lang)
        if args.validate:
            validate(lang, mapping)
            print(f"Validated {hub_filename(lang)}")
            continue

        (ROOT / hub_filename(lang)).write_text(render_hub_page(lang, mapping), encoding="utf-8", newline="\n")
        detail_filenames = []
        page_index = 0
        for region_name, region_filename, districts in mapping:
            for source_filename, district_name in districts:
                filename = detail_filename(lang, source_filename)
                detail_filenames.append(filename)
                (ROOT / filename).write_text(
                    render_district_page(lang, region_name, region_filename, district_name, source_filename, page_index),
                    encoding="utf-8",
                    newline="\n",
                )
                page_index += 1
        add_hub_link(lang)
        update_sitemap(lang, detail_filenames)
        validate(lang, mapping)
        print(f"Generated {hub_filename(lang)} and {len(detail_filenames)} district pages")


if __name__ == "__main__":
    main()
