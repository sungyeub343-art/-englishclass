from argparse import ArgumentParser
from datetime import date
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from generate_japanese_exam_pages import shared_head, structured_data, styles


ROOT = Path(__file__).parent
SITE_URL = "https://englishclass.kr"
HUB_FILENAME = "chinese-exam-guide.html"
TITLE = "지역별 + HSK HSKK TSC BCT 무료체험 안내"
EXPECTED_REGION_COUNT = 17
EXPECTED_DISTRICT_COUNT = 229
# The shared styles lay out five exam cards; the Chinese pages show four.
SUMMARY_CSS = "<style>@media (min-width:921px){.summary{grid-template-columns:repeat(4,minmax(0,1fr))}}</style>"


def exam_filename(source_filename: str) -> str:
    return source_filename.replace("chinese-", "chinese-exam-", 1)


def region_map() -> list[tuple[str, str, list[tuple[str, str]]]]:
    index_text = (ROOT / "chinese.html").read_text(encoding="utf-8")
    regions = re.findall(
        r"class='region-card' href='(chinese-[^']+\.html)'><strong>([^<]+)</strong>",
        index_text,
    )
    if len(regions) != EXPECTED_REGION_COUNT:
        raise ValueError(f"Expected {EXPECTED_REGION_COUNT} regions, got {len(regions)}")

    mapping = []
    for region_filename, region_name in regions:
        region_text = (ROOT / region_filename).read_text(encoding="utf-8")
        districts = re.findall(
            r"class='chip' href='(chinese-[^']+\.html)'>([^<]+)</a>",
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


def render_hub(mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> str:
    sections = []
    for region_name, region_filename, districts in mapping:
        links = "\n".join(
            f'          <a href="{exam_filename(filename)}">{escape(district_name)} HSK HSKK TSC BCT 안내</a>'
            for filename, district_name in districts
        )
        sections.append(f'''      <section class="region-group" data-region="{escape(region_name)}">
        <div class="region-heading"><h2>{escape(region_name)}</h2><a href="{region_filename}">{escape(region_name)} 중국어회화 보기</a></div>
        <div class="district-grid">
{links}
        </div>
      </section>''')
    description = "전국 229개 시·군·구별 HSK, HSKK, TSC, BCT 중국어 시험 준비와 1:1 화상 중국어 무료체험을 안내합니다."
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
{shared_head(TITLE, description, HUB_FILENAME, "website")}
{styles(1180)}
{structured_data(TITLE, description, HUB_FILENAME)}
</head>
<body>
<header><div class="wrap nav"><a class="logo" href="index.html"><span>파워</span>잉글리쉬</a><nav class="nav-links" aria-label="주요 메뉴"><a href="chinese.html">중국어회화 지역 보기</a><a class="apply" href="index.html#apply">무료체험 신청</a></nav></div></header>
<main>
  <section class="hero"><div class="wrap">
    <p class="eyebrow">전국 229개 시·군·구 중국어 시험 대비</p>
    <h1>{TITLE}</h1>
    <p class="lead">거주 지역을 선택해 HSK, HSKK, TSC, BCT 목표에 맞는 학습 방향을 확인하세요. 시험 종류와 현재 수준을 바탕으로 1:1 화상 중국어 무료체험 수업을 안내합니다.</p>
    <div class="actions"><a class="button primary" href="#regions">지역 선택하기</a><a class="button secondary" href="index.html#apply">무료체험 신청</a></div>
  </div></section>
  <section class="finder" id="regions"><div class="wrap">
    <div class="finder-head"><div><h2>시·군·구별 중국어 시험 안내</h2><p>원하는 시·군·구를 선택해 네 시험의 특징과 맞춤 준비 방법을 확인하세요.</p></div><div><label class="search-label" for="district-search">시·군·구 찾기</label><input id="district-search" type="search" placeholder="예: 종로구, 수원시, 해운대구" autocomplete="off"></div></div>
{chr(10).join(sections)}
    <p class="no-results" role="status">일치하는 지역이 없습니다. 시·군·구 이름을 다시 확인해 주세요.</p>
  </div></section>
  <section class="cta"><div class="wrap cta-inner"><div><h2>어떤 중국어 시험이 맞는지 확인하세요</h2><p>목표와 현재 수준을 확인한 뒤 시험별 학습 방향을 안내합니다.</p></div><a class="button" href="index.html#apply">무료체험 신청</a></div></section>
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
    title = f"{location} HSK HSKK TSC BCT 무료체험 안내"
    description = f"{location} HSK, HSKK, TSC, BCT 시험별 준비 방법과 1:1 화상 중국어 무료체험 수업을 안내합니다."
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
{shared_head(title, description, filename, "article")}
{styles(1040)}
{SUMMARY_CSS}
{structured_data(title, description, filename)}
</head>
<body>
<header><div class="wrap nav"><a class="logo" href="index.html"><span>파워</span>잉글리쉬</a><nav class="nav-links" aria-label="주요 메뉴"><a href="{HUB_FILENAME}">전국 시험 안내</a><a class="apply" href="index.html#apply">무료체험 신청</a></nav></div></header>
<main>
  <div class="wrap breadcrumb" aria-label="빵부스러기"><a href="index.html">홈</a><span>›</span><a href="{HUB_FILENAME}">중국어 시험 안내</a><span>›</span><a href="{region_filename}">{escape(region_name)}</a><span>›</span><span>{escape(district_name)}</span></div>
  <section class="hero"><div class="wrap">
    <p class="eyebrow">{escape(location)} · 1:1 화상 중국어 시험 대비</p>
    <h1>{escape(title)}</h1>
    <p class="lead">같은 중국어 시험이라도 필기와 말하기, 일반 중국어와 비즈니스 중국어처럼 평가 방식과 활용 목적이 다릅니다. {escape(location)} 학습자의 목표 시험, 응시 일정, 현재 실력을 확인해 우선 준비할 영역과 수업 방향을 안내합니다.</p>
    <div class="actions"><a class="button primary" href="index.html#apply">무료체험 신청</a><a class="button secondary" href="{source_filename}">{escape(location)} 중국어회화 보기</a></div>
  </div></section>
  <section class="visual"><div class="wrap"><img src="[복사본] 파워CH 중국어.jpg" alt="{escape(location)} HSK HSKK TSC BCT 무료체험 안내 이미지" width="1080" height="10800" loading="lazy" decoding="async"></div></section>
  <section><div class="wrap summary">
    <article><h2>HSK</h2><p>급수별로 듣기, 독해, 쓰기 영역을 나누어 어휘와 문법을 체계적으로 준비합니다.</p></article>
    <article><h2>HSKK</h2><p>들은 내용을 따라 말하고 질문에 답하는 중국어 말하기 시험을 단계별로 대비합니다.</p></article>
    <article><h2>TSC</h2><p>자기소개, 그림 묘사, 상황 대응, 의견 제시 등 실전 말하기 문항을 훈련합니다.</p></article>
    <article><h2>BCT</h2><p>회의, 거래, 출장 등 비즈니스 상황에서 쓰는 중국어 이해와 표현을 다룹니다.</p></article>
  </div></section>
  <section class="content"><div class="wrap content-grid">
    <article class="panel">
      <span class="label">시험별 목표 진단</span>
      <h2>{escape(location)} 중국어 시험 준비, 평가 방식부터 구분하세요</h2>
      <p>HSK는 듣기, 독해, 쓰기를 급수별로 평가하는 필기 시험이고, HSKK와 TSC는 실제로 말한 답변을 평가하는 말하기 시험입니다. BCT는 업무 장면에서 중국어 정보를 이해하고 응대하는 능력을 봅니다. 같은 학습 시간이라도 어떤 시험을 준비하느냐에 따라 우선순위가 달라집니다.</p>
      <h3>HSK 급수별 필기 준비</h3>
      <p>목표 급수와 시험일까지 남은 기간을 기준으로 어휘, 문법, 독해, 듣기의 우선순위를 정합니다. 오답 개수만 확인하지 않고 선택지를 잘못 판단한 이유와 시간이 부족했던 구간을 점검해 복습 범위를 좁힙니다.</p>
      <h3>HSKK·TSC 말하기와 성조 교정</h3>
      <p>말하기 시험은 알고 있는 표현을 제한 시간 안에 직접 말하는 연습이 핵심입니다. 1:1 화상 수업에서 문항 유형별 답변 구조를 익히고, 성조와 발음, 문장 연결을 실시간으로 교정해 답변의 정확도와 유창성을 함께 높입니다.</p>
      <h3>BCT 비즈니스 중국어와 무료체험</h3>
      <p>BCT는 회의, 이메일, 전화, 거래 조건 등 업무 맥락을 이해하는 연습이 필요합니다. 무료체험에서는 자기소개와 상황 응답으로 현재 수준을 확인하고, 취업·승진·주재원 파견 등 시험 목적에 맞춰 수업 방향을 안내합니다.</p>
    </article>
    <aside class="panel"><h2>무료체험 전에 알려주세요</h2><ul><li>준비 중인 시험과 목표 급수 또는 점수</li><li>응시 예정일과 주당 학습 가능 시간</li><li>최근 모의고사 또는 시험 결과</li><li>어휘, 독해, 듣기, 말하기 중 어려운 영역</li><li>유학, 취업, 승진 등 시험을 준비하는 목적</li></ul></aside>
  </div></section>
  <section class="cta"><div class="wrap cta-inner"><div><h2>{escape(location)} 중국어 시험 무료체험</h2><p>현재 수준과 목표 시험을 확인하고 필요한 영역부터 준비하세요.</p></div><a class="button" href="index.html#apply">무료체험 신청</a></div></section>
</main>
<footer><div class="wrap">© 2026 파워잉글리쉬 · {escape(title)}</div></footer>
</body>
</html>
'''


def add_hub_link() -> None:
    path = ROOT / "chinese.html"
    text = path.read_text(encoding="utf-8")
    if f'href="{HUB_FILENAME}"' in text:
        return
    anchor = '    <div class="region-grid">\n'
    if '<a class="business-inquiry"' not in text or anchor not in text:
        raise ValueError("Business inquiry block not found in chinese.html")
    link = f'''    <a class="business-inquiry" href="{HUB_FILENAME}">
      <span><strong>지역별(시군구) + HSK HSKK TSC BCT 시험 안내</strong><span>전국 229개 시·군·구에서 중국어 시험 맞춤 상담 페이지를 찾아보세요.</span></span>
      <b>지역 선택하기 →</b>
    </a>
'''
    path.write_text(text.replace(anchor, link + anchor, 1), encoding="utf-8", newline="\n")


def update_sitemap(detail_filenames: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    url_pattern = rf"{re.escape(SITE_URL)}/(?:{re.escape(HUB_FILENAME)}|chinese-exam-[^<]+\.html)"
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
    actual_links = set(re.findall(r'<a href="(chinese-exam-[^"]+\.html)">[^<]+ HSK HSKK TSC BCT 안내</a>', hub_text))
    if actual_links != expected_links:
        raise ValueError("Missing or unexpected district links")
    if f"<title>{TITLE}</title>" not in hub_text or f"<h1>{TITLE}</h1>" not in hub_text:
        raise ValueError("Required hub title is missing")
    if f'<link rel="canonical" href="{SITE_URL}/{HUB_FILENAME}">' not in hub_text:
        raise ValueError("Invalid hub canonical URL")
    if f'href="{HUB_FILENAME}"' not in (ROOT / "chinese.html").read_text(encoding="utf-8"):
        raise ValueError("Missing hub link in chinese.html")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    expected_urls = {f"{SITE_URL}/{filename}" for filename in expected_links}
    actual_urls = {
        url for url in urls
        if url and "/chinese-exam-" in url and url != f"{SITE_URL}/{HUB_FILENAME}"
    }
    if urls.count(f"{SITE_URL}/{HUB_FILENAME}") != 1 or actual_urls != expected_urls:
        raise ValueError("Invalid sitemap entries")

    for region_name, _, districts in mapping:
        for source_filename, district_name in districts:
            filename = exam_filename(source_filename)
            detail_text = (ROOT / filename).read_text(encoding="utf-8")
            title = f"{region_name} {district_name} HSK HSKK TSC BCT 무료체험 안내"
            expected_url = f"{SITE_URL}/{filename}"
            if f"<title>{title}</title>" not in detail_text or f"<h1>{title}</h1>" not in detail_text:
                raise ValueError(f"Invalid title in {filename}")
            if detail_text.count(f'<link rel="canonical" href="{expected_url}">') != 1:
                raise ValueError(f"Invalid canonical URL in {filename}")
            if f'href="{source_filename}"' not in detail_text:
                raise ValueError(f"Missing Chinese source link in {filename}")


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
    add_hub_link()
    update_sitemap(detail_filenames)
    validate(mapping)
    print(f"Generated {HUB_FILENAME} and {len(detail_filenames)} district pages")
    print("Updated and validated sitemap.xml")


if __name__ == "__main__":
    main()
