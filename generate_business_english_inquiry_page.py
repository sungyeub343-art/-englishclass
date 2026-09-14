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
            f'          <a href="{filename}">{escape(district_name)} 직장인 영어스피킹 문의</a>'
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


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    url = f"{SITE_URL}/{FILENAME}"
    text = re.sub(
        rf"\s*<url>\s*<loc>{re.escape(url)}</loc>.*?</url>",
        "",
        text,
        flags=re.S,
    )
    entry = f'''  <url>
    <loc>{url}</loc>
    <lastmod>{date.today().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
'''
    text = text.replace("</urlset>", entry + "</urlset>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate(mapping: list[tuple[str, str, list[tuple[str, str]]]]) -> None:
    path = ROOT / FILENAME
    text = path.read_text(encoding="utf-8")
    expected_links = {
        filename
        for _, _, districts in mapping
        for filename, _ in districts
    }
    actual_links = set(re.findall(r'<a href="(english-[^"]+\.html)">[^<]+ 직장인 영어스피킹 문의</a>', text))
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
    update_sitemap()
    validate(mapping)
    print(f"Generated {FILENAME} with {EXPECTED_DISTRICT_COUNT} district links")
    print("Updated and validated sitemap.xml")


if __name__ == "__main__":
    main()