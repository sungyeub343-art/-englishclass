from argparse import ArgumentParser
from datetime import date
from html import escape
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent
SITE_URL = "https://englishclass.kr"
HUB_FILENAME = "japanese-exam-guide.html"
TITLE = "지역별 + JLPT JPT BJT EJU SJPT 무료체험 안내"
EXPECTED_REGION_COUNT = 17
EXPECTED_DISTRICT_COUNT = 229


def exam_filename(source_filename: str) -> str:
    return source_filename.replace("japanese-", "japanese-exam-", 1)


def region_map() -> list[tuple[str, str, list[tuple[str, str]]]]:
    index_text = (ROOT / "japanese.html").read_text(encoding="utf-8")
    regions = re.findall(
        r"class='region-card' href='(japanese-[^']+\.html)'><strong>([^<]+)</strong>",
        index_text,
    )
    if len(regions) != EXPECTED_REGION_COUNT:
        raise ValueError(f"Expected {EXPECTED_REGION_COUNT} regions, got {len(regions)}")

    mapping = []
    for region_filename, region_name in regions:
        region_text = (ROOT / region_filename).read_text(encoding="utf-8")
        districts = re.findall(
            r"class='chip' href='(japanese-[^']+\.html)'>([^<]+)</a>",
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


def shared_head(title: str, description: str, filename: str, page_type: str) -> str:
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/{filename}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="{page_type}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{SITE_URL}/{filename}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{SITE_URL}/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">'''


def styles(max_width: int) -> str:
    return f'''<style>
:root{{--bg:#f4f3ee;--ink:#182238;--muted:#5d6678;--line:#d9d6cc;--accent:#c94432;--accent-dark:#8f2d25;--paper:#fff;--soft:#eef4f2;--maxw:{max_width}px}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;font-family:'Noto Sans KR',sans-serif;color:var(--ink);background:linear-gradient(155deg,var(--bg) 0,var(--soft) 54%,#f7f6f2 100%)}}
a{{color:inherit;text-decoration:none}}.wrap{{width:min(100% - 40px,var(--maxw));margin:0 auto}}
header{{position:sticky;top:0;z-index:10;border-bottom:1px solid var(--line);background:rgba(244,243,238,.95);backdrop-filter:blur(8px)}}
.nav{{min-height:68px;display:flex;align-items:center;justify-content:space-between;gap:18px}}.logo{{font:700 27px/1 'Fraunces',serif}}.logo span{{color:var(--accent)}}
.nav-links{{display:flex;align-items:center;gap:16px;color:var(--muted);font-size:14px;font-weight:700}}.nav-links .apply{{padding:10px 15px;border-radius:6px;background:var(--ink);color:#fff}}
.breadcrumb{{display:flex;flex-wrap:wrap;gap:7px;padding-top:16px;color:var(--muted);font-size:13px}}
.hero{{padding:58px 0 38px}}.eyebrow{{margin:0 0 13px;color:var(--accent-dark);font-weight:800}}
h1{{max-width:960px;margin:0;font:700 clamp(34px,6vw,64px)/1.14 'Fraunces','Noto Sans KR',serif;letter-spacing:0}}
.lead{{max-width:800px;margin:20px 0 0;color:var(--muted);font-size:17px;line-height:1.8}}
.actions{{display:flex;flex-wrap:wrap;gap:10px;margin-top:25px}}.button{{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 18px;border-radius:6px;font-weight:800}}
.button.primary{{background:var(--accent);color:#fff}}.button.secondary{{border:1px solid var(--line);background:#fff}}
.visual{{padding:0 0 40px}}.visual img{{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px}}
.summary{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;padding:0 0 42px}}.summary article{{padding:18px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}}
.summary h2{{margin:0 0 8px;font-size:18px}}.summary p{{margin:0;color:var(--muted);font-size:13px;line-height:1.65}}
.content{{padding:4px 0 60px}}.content-grid{{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(270px,.65fr);gap:18px}}
.panel{{padding:26px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}}.panel h2{{margin:0 0 14px;font-size:25px;line-height:1.4}}.panel h3{{margin:24px 0 8px;font-size:18px}}
.panel p{{margin:0 0 13px;color:var(--muted);line-height:1.85}}.panel ul{{margin:0;padding-left:20px;color:var(--muted)}}.panel li{{margin:0 0 12px;line-height:1.75}}
.label{{display:inline-block;margin-bottom:14px;padding:7px 10px;background:#fff0ec;color:var(--accent-dark);font-size:13px;font-weight:800}}
.finder{{padding:22px 0 72px}}.finder-head{{display:grid;grid-template-columns:1fr minmax(280px,420px);gap:28px;align-items:end;margin-bottom:28px}}.finder h2{{margin:0;font-size:30px}}.finder-head p{{margin:8px 0 0;color:var(--muted);line-height:1.7}}
.search-label{{display:block;margin-bottom:8px;color:var(--muted);font-size:13px;font-weight:800}}#district-search{{width:100%;height:48px;padding:0 14px;border:1px solid #bfc5c8;border-radius:6px;background:#fff;font:500 16px 'Noto Sans KR',sans-serif}}#district-search:focus{{outline:3px solid rgba(201,68,50,.2);border-color:var(--accent)}}
.region-group{{padding:25px 0;border-top:1px solid var(--line)}}.region-heading{{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:14px}}.region-heading h2{{margin:0;font-size:24px}}.region-heading a{{color:var(--accent-dark);font-size:14px;font-weight:800}}
.district-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}}.district-grid a{{display:flex;align-items:center;min-height:48px;padding:10px 12px;border:1px solid var(--line);border-radius:6px;background:#fff;font-size:14px;font-weight:700;line-height:1.45}}.district-grid a:hover{{border-color:var(--accent);color:var(--accent-dark)}}.no-results{{display:none;padding:28px 0;border-top:1px solid var(--line);color:var(--muted);font-weight:700}}
.cta{{padding:46px 0;background:var(--ink);color:#fff}}.cta-inner{{display:flex;align-items:center;justify-content:space-between;gap:22px}}.cta h2{{margin:0 0 7px;font-size:27px}}.cta p{{margin:0;color:#cdd3df;line-height:1.7}}.cta .button{{flex:0 0 auto;background:#fff;color:var(--ink)}}footer{{padding:30px 0;color:#747d90;font-size:13px}}
@media (max-width:920px){{.summary{{grid-template-columns:repeat(2,minmax(0,1fr))}}.district-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.finder-head,.content-grid{{grid-template-columns:1fr}}}}
@media (max-width:560px){{.wrap{{width:min(100% - 28px,var(--maxw))}}.nav{{align-items:flex-start;padding:16px 0}}.nav-links{{justify-content:flex-end;flex-wrap:wrap}}.nav-links a:first-child{{display:none}}.hero{{padding-top:42px}}.lead{{font-size:15px}}.summary,.district-grid{{grid-template-columns:1fr}}.panel{{padding:20px}}.cta-inner{{align-items:flex-start;flex-direction:column}}}}
</style>'''


def structured_data(title: str, description: str, filename: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": f"{SITE_URL}/{filename}",
        "description": description,
        "inLanguage": "ko-KR",
        "publisher": {
            "@type": "Organization",
            "name": "파워잉글리쉬",
            "url": f"{SITE_URL}/",
        },
    }
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + "</script>"


def render_hub(mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> str:
    sections = []
    for region_name, region_filename, districts in mapping:
        links = "\n".join(
            f'          <a href="{exam_filename(filename)}">{escape(district_name)} JLPT JPT BJT EJU SJPT 안내</a>'
            for filename, district_name in districts
        )
        sections.append(f'''      <section class="region-group" data-region="{escape(region_name)}">
        <div class="region-heading"><h2>{escape(region_name)}</h2><a href="{region_filename}">{escape(region_name)} 일본어회화 보기</a></div>
        <div class="district-grid">
{links}
        </div>
      </section>''')
    description = "전국 229개 시·군·구별 JLPT, JPT, BJT, EJU, SJPT 일본어 시험 준비와 1:1 화상 일본어 무료체험을 안내합니다."
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
{shared_head(TITLE, description, HUB_FILENAME, "website")}
{styles(1180)}
{structured_data(TITLE, description, HUB_FILENAME)}
</head>
<body>
<header><div class="wrap nav"><a class="logo" href="index.html"><span>파워</span>잉글리쉬</a><nav class="nav-links" aria-label="주요 메뉴"><a href="japanese.html">일본어회화 지역 보기</a><a class="apply" href="index.html#apply">무료체험 신청</a></nav></div></header>
<main>
  <section class="hero"><div class="wrap">
    <p class="eyebrow">전국 229개 시·군·구 일본어 시험 대비</p>
    <h1>{TITLE}</h1>
    <p class="lead">거주 지역을 선택해 JLPT, JPT, BJT, EJU, SJPT 목표에 맞는 학습 방향을 확인하세요. 시험 종류와 현재 수준을 바탕으로 1:1 화상 일본어 무료체험 수업을 안내합니다.</p>
    <div class="actions"><a class="button primary" href="#regions">지역 선택하기</a><a class="button secondary" href="index.html#apply">무료체험 신청</a></div>
  </div></section>
  <section class="finder" id="regions"><div class="wrap">
    <div class="finder-head"><div><h2>시·군·구별 일본어 시험 안내</h2><p>원하는 시·군·구를 선택해 다섯 시험의 특징과 맞춤 준비 방법을 확인하세요.</p></div><div><label class="search-label" for="district-search">시·군·구 찾기</label><input id="district-search" type="search" placeholder="예: 종로구, 수원시, 해운대구" autocomplete="off"></div></div>
{chr(10).join(sections)}
    <p class="no-results" role="status">일치하는 지역이 없습니다. 시·군·구 이름을 다시 확인해 주세요.</p>
  </div></section>
  <section class="cta"><div class="wrap cta-inner"><div><h2>어떤 일본어 시험이 맞는지 확인하세요</h2><p>목표와 현재 수준을 확인한 뒤 시험별 학습 방향을 안내합니다.</p></div><a class="button" href="index.html#apply">무료체험 신청</a></div></section>
</main>
<footer><div class="wrap">© 2026 파워잉글리쉬 · {TITLE}</div></footer>
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
) -> str:
    location = f"{region_name} {district_name}"
    filename = exam_filename(source_filename)
    title = f"{location} JLPT JPT BJT EJU SJPT 무료체험 안내"
    description = f"{location} JLPT, JPT, BJT, EJU, SJPT 시험별 준비 방법과 1:1 화상 일본어 무료체험 수업을 안내합니다."
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
{shared_head(title, description, filename, "article")}
{styles(1040)}
{structured_data(title, description, filename)}
</head>
<body>
<header><div class="wrap nav"><a class="logo" href="index.html"><span>파워</span>잉글리쉬</a><nav class="nav-links" aria-label="주요 메뉴"><a href="{HUB_FILENAME}">전국 시험 안내</a><a class="apply" href="index.html#apply">무료체험 신청</a></nav></div></header>
<main>
  <div class="wrap breadcrumb" aria-label="빵부스러기"><a href="index.html">홈</a><span>›</span><a href="{HUB_FILENAME}">일본어 시험 안내</a><span>›</span><a href="{region_filename}">{escape(region_name)}</a><span>›</span><span>{escape(district_name)}</span></div>
  <section class="hero"><div class="wrap">
    <p class="eyebrow">{escape(location)} · 1:1 화상 일본어 시험 대비</p>
    <h1>{escape(title)}</h1>
    <p class="lead">시험 이름은 비슷해 보여도 평가 영역과 활용 목적은 다릅니다. {escape(location)} 학습자의 목표 시험, 응시 일정, 현재 실력을 확인해 우선 준비할 영역과 수업 방향을 안내합니다.</p>
    <div class="actions"><a class="button primary" href="index.html#apply">무료체험 신청</a><a class="button secondary" href="{source_filename}">{escape(location)} 일본어회화 보기</a></div>
  </div></section>
  <section class="visual"><div class="wrap"><img src="[복사본] 파워JP 일본어.jpg" alt="{escape(location)} JLPT JPT BJT EJU SJPT 무료체험 안내 이미지" width="1080" height="12960" loading="lazy" decoding="async"></div></section>
  <section><div class="wrap summary">
    <article><h2>JLPT</h2><p>N1부터 N5까지 언어지식, 독해, 청해 영역을 수준별로 준비합니다.</p></article>
    <article><h2>JPT</h2><p>하나의 점수 체계로 평가하는 청해와 독해의 속도와 정확도를 높입니다.</p></article>
    <article><h2>BJT</h2><p>비즈니스 상황의 정보 이해, 판단, 응대에 필요한 일본어를 다룹니다.</p></article>
    <article><h2>EJU</h2><p>일본 유학과 대학 수학에 필요한 일본어 독해, 청해·청독해를 준비합니다.</p></article>
    <article><h2>SJPT</h2><p>질문에 바로 응답하고 의견을 설명하는 일본어 말하기 능력을 훈련합니다.</p></article>
  </div></section>
  <section class="content"><div class="wrap content-grid">
    <article class="panel">
      <span class="label">시험별 목표 진단</span>
      <h2>{escape(location)} 일본어 시험 준비, 평가 방식부터 구분하세요</h2>
      <p>JLPT와 JPT는 어휘·문법·독해·청해를 중심으로 준비하지만 등급과 점수 체계가 다릅니다. BJT는 업무 장면에서 정보를 이해하고 적절하게 판단하는 능력을, EJU 일본어 과목은 일본 대학에서 공부하는 데 필요한 학업 일본어를 평가합니다. SJPT는 실제로 말한 답변을 평가하므로 발음, 응답 속도, 문장 구성 훈련이 중요합니다.</p>
      <h3>JLPT·JPT 듣기와 읽기 준비</h3>
      <p>목표 등급이나 점수와 시험일까지 남은 기간을 기준으로 어휘, 문법, 독해, 청해의 우선순위를 정합니다. 오답 개수만 확인하지 않고 선택지를 잘못 판단한 이유와 시간 부족이 생긴 구간을 점검해 복습 범위를 좁힙니다.</p>
      <h3>BJT·EJU 목적별 일본어 준비</h3>
      <p>BJT는 회의, 보고, 전화, 이메일 등 비즈니스 맥락을 이해하는 연습이 필요합니다. EJU는 대학 강의와 자료에서 핵심 정보를 파악하고 논리적으로 정리하는 학업 일본어가 중요하므로 진학 목표와 수험 과목을 상담에서 함께 확인합니다.</p>
      <h3>SJPT 말하기와 무료체험</h3>
      <p>SJPT는 알고 있는 표현을 제한 시간 안에 직접 말하는 연습이 핵심입니다. 무료체험에서는 자기소개, 상황 응답, 의견 설명을 통해 현재 발화 수준을 확인하고, 1:1 화상 수업에서 보완할 발음과 문장 연결 방식을 안내합니다.</p>
    </article>
    <aside class="panel"><h2>무료체험 전에 알려주세요</h2><ul><li>준비 중인 시험과 목표 등급 또는 점수</li><li>응시 예정일과 주당 학습 가능 시간</li><li>최근 모의고사 또는 시험 결과</li><li>어휘, 독해, 청해, 말하기 중 어려운 영역</li><li>유학, 취업, 승진 등 시험을 준비하는 목적</li></ul></aside>
  </div></section>
  <section class="cta"><div class="wrap cta-inner"><div><h2>{escape(location)} 일본어 시험 무료체험</h2><p>현재 수준과 목표 시험을 확인하고 필요한 영역부터 준비하세요.</p></div><a class="button" href="index.html#apply">무료체험 신청</a></div></section>
</main>
<footer><div class="wrap">© 2026 파워잉글리쉬 · {escape(title)}</div></footer>
</body>
</html>
'''


def update_sitemap(detail_filenames: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    url_pattern = rf"{re.escape(SITE_URL)}/(?:{re.escape(HUB_FILENAME)}|japanese-exam-[^<]+\.html)"
    text = re.sub(
        rf"\s*<url>\s*<loc>{url_pattern}</loc>.*?</url>",
        "",
        text,
        flags=re.S,
    )
    urls = [HUB_FILENAME, *detail_filenames]
    entries = "".join(f'''  <url>
    <loc>{SITE_URL}/{filename}</loc>
    <lastmod>{date.today().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"0.9" if filename == HUB_FILENAME else "0.7"}</priority>
  </url>
''' for filename in urls)
    text = text.replace("</urlset>", entries + "</urlset>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate(mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> None:
    hub_text = (ROOT / HUB_FILENAME).read_text(encoding="utf-8")
    expected_links = {
        exam_filename(filename)
        for _, _, districts in mapping
        for filename, _ in districts
    }
    actual_links = set(re.findall(r'<a href="(japanese-exam-[^"]+\.html)">[^<]+ JLPT JPT BJT EJU SJPT 안내</a>', hub_text))
    if actual_links != expected_links:
        raise ValueError("Missing or unexpected district links")
    if f"<title>{TITLE}</title>" not in hub_text or f"<h1>{TITLE}</h1>" not in hub_text:
        raise ValueError("Required hub title is missing")
    if f'<link rel="canonical" href="{SITE_URL}/{HUB_FILENAME}">' not in hub_text:
        raise ValueError("Invalid hub canonical URL")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    expected_urls = {f"{SITE_URL}/{filename}" for filename in expected_links}
    actual_urls = {
        url for url in urls
        if url and "/japanese-exam-" in url and url != f"{SITE_URL}/{HUB_FILENAME}"
    }
    if urls.count(f"{SITE_URL}/{HUB_FILENAME}") != 1 or actual_urls != expected_urls:
        raise ValueError("Invalid sitemap entries")

    for region_name, _, districts in mapping:
        for source_filename, district_name in districts:
            filename = exam_filename(source_filename)
            detail_text = (ROOT / filename).read_text(encoding="utf-8")
            title = f"{region_name} {district_name} JLPT JPT BJT EJU SJPT 무료체험 안내"
            expected_url = f"{SITE_URL}/{filename}"
            if f"<title>{title}</title>" not in detail_text or f"<h1>{title}</h1>" not in detail_text:
                raise ValueError(f"Invalid title in {filename}")
            if detail_text.count(f'<link rel="canonical" href="{expected_url}">') != 1:
                raise ValueError(f"Invalid canonical URL in {filename}")
            if f'href="{source_filename}"' not in detail_text:
                raise ValueError(f"Missing Japanese source link in {filename}")


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
        print(f"Validated {HUB_FILENAME} with {EXPECTED_DISTRICT_COUNT} district links")
        return

    (ROOT / HUB_FILENAME).write_text(render_hub(mapping), encoding="utf-8", newline="\n")
    detail_filenames = []
    for region_name, region_filename, districts in mapping:
        for source_filename, district_name in districts:
            filename = exam_filename(source_filename)
            detail_filenames.append(filename)
            (ROOT / filename).write_text(
                render_district_page(region_name, region_filename, district_name, source_filename),
                encoding="utf-8",
                newline="\n",
            )
    update_sitemap(detail_filenames)
    validate(mapping)
    print(f"Generated {HUB_FILENAME} and {len(detail_filenames)} district pages")
    print("Updated and validated sitemap.xml")


if __name__ == "__main__":
    main()