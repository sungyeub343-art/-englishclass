from datetime import date
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent

# Administrative 읍면동 names for the 9 Daegu districts and counties.
DISTRICTS = {
    "jung": ("중구", [
        "동인동", "삼덕동", "성내1동", "성내2동", "성내3동", "대신동",
        "남산1동", "남산2동", "남산3동", "남산4동", "대봉1동", "대봉2동",
    ]),
    "dong": ("동구", [
        "신암1동", "신암2동", "신암3동", "신암4동", "신암5동", "신천1·2동",
        "신천3동", "신천4동", "효목1동", "효목2동", "도평동", "불로봉무동",
        "지저동", "동촌동", "방촌동", "해안동", "안심1동", "안심2동",
        "안심3동", "안심4동", "혁신동", "공산동",
    ]),
    "seo": ("서구", [
        "내당1동", "내당2·3동", "내당4동", "비산1동", "비산2·3동", "비산4동",
        "비산5동", "비산6동", "비산7동", "평리1동", "평리2동", "평리3동",
        "평리4동", "평리5동", "평리6동", "상중이동", "원대동",
    ]),
    "nam": ("남구", [
        "이천동", "봉덕1동", "봉덕2동", "봉덕3동", "대명1동", "대명2동",
        "대명3동", "대명4동", "대명5동", "대명6동", "대명9동", "대명10동", "대명11동",
    ]),
    "buk": ("북구", [
        "고성동", "칠성동", "침산1동", "침산2동", "침산3동", "노원동",
        "산격1동", "산격2동", "산격3동", "산격4동", "복현1동", "복현2동",
        "대현동", "검단동", "무태조야동", "관문동", "태전1동", "태전2동",
        "구암동", "관음동", "읍내동", "동천동", "국우동",
    ]),
    "suseong": ("수성구", [
        "범어1동", "범어2동", "범어3동", "범어4동", "만촌1동", "만촌2동",
        "만촌3동", "수성1가동", "수성2·3가동", "수성4가동", "황금1동", "황금2동",
        "중동", "상동", "파동", "두산동", "지산1동", "지산2동", "범물1동",
        "범물2동", "고산1동", "고산2동", "고산3동",
    ]),
    "dalseo": ("달서구", [
        "성당동", "두류1·2동", "두류3동", "본리동", "감삼동", "죽전동", "장기동",
        "용산1동", "용산2동", "이곡1동", "이곡2동", "신당동", "월성1동", "월성2동",
        "진천동", "유천동", "상인1동", "상인2동", "상인3동", "도원동", "송현1동",
        "송현2동", "본동",
    ]),
    "dalseong": ("달성군", [
        "화원읍", "논공읍", "다사읍", "유가읍", "옥포읍", "현풍읍", "가창면", "하빈면", "구지면",
    ]),
    "gunwi": ("군위군", [
        "군위읍", "소보면", "효령면", "부계면", "우보면", "의흥면", "산성면", "삼국유사면",
    ]),
}

EXPECTED_PAGE_COUNT = 150

CSS = ".subdistricts{margin-top:24px;padding-top:20px;border-top:1px solid var(--line)}.subdistricts h2{margin:0 0 12px;font-size:19px}.subdistrict-links{display:flex;flex-wrap:wrap;gap:8px}.subdistrict-links a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:#2f3f61;font-size:13px;font-weight:700}"


def remove_subdistricts(text: str) -> str:
    text = text.replace(CSS, "", 1)
    return re.sub(r'\n?\s*<div class="subdistricts">.*?</div>\s*</div>', "", text, count=1, flags=re.S)


def child_from_parent(source: str, district_name: str, locality: str, filename: str, parent_filename: str) -> str:
    text = remove_subdistricts(source)
    parent_label = f"대구 {district_name}"
    label = f"{parent_label} {locality}"
    text = text.replace(parent_label, label)
    text = text.replace(
        f'https://englishclass.kr/{parent_filename}',
        f'https://englishclass.kr/{filename}',
    )
    text = text.replace(
        f'<span>{district_name}</span>',
        f'<a href="{parent_filename}">{district_name}</a>\n      <span>›</span>\n      <span>{locality}</span>',
        1,
    )
    text = text.replace(
        '<a class="btn ghost" href="english-daegu.html">대구 시·군·구 전체 보기</a>',
        f'<a class="btn ghost" href="{parent_filename}">{district_name} 전체 읍면동 보기</a>',
        1,
    )
    return text


def update_parent(slug: str, district_name: str, localities: list[str]) -> str:
    parent = ROOT / f"english-daegu-{slug}.html"
    if not parent.exists():
        raise FileNotFoundError(parent)

    source = parent.read_text(encoding="utf-8")
    text = source
    if ".subdistricts{" not in text:
        text = text.replace(".photo-strip{", CSS + ".photo-strip{", 1)

    links = "\n".join(
        f'        <a href="english-daegu-{slug}-{index}.html">{locality}</a>'
        for index, locality in enumerate(localities, 1)
    )
    block = f'''    <div class="subdistricts">
      <h2>대구 {district_name} 읍면동 영어회화</h2>
      <div class="subdistrict-links">
{links}
      </div>
    </div>
'''
    if '<div class="subdistricts">' in text:
        text = re.sub(
            r'    <div class="subdistricts">.*?    </div>\n',
            block,
            text,
            count=1,
            flags=re.S,
        )
    else:
        marker = "    </div>\n  </div>\n</section>\n</main>"
        if marker not in text:
            raise ValueError(f"CTA marker not found in {parent.name}")
        text = text.replace(marker, "    </div>\n" + block + "  </div>\n</section>\n</main>", 1)

    parent.write_text(text, encoding="utf-8", newline="\n")
    return source


def update_sitemap(filenames: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'\s*<url>\s*<loc>https://englishclass\.kr/english-daegu-[^<]+-\d+\.html</loc>.*?</url>',
        "",
        text,
        flags=re.S,
    )
    today = date.today().isoformat()
    entries = "\n".join(
        f'''  <url>
    <loc>https://englishclass.kr/{filename}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>'''
        for filename in filenames
    )
    text = text.replace("</urlset>", entries + "\n</urlset>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate_output(filenames: list[str]) -> None:
    if len(filenames) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"Expected {EXPECTED_PAGE_COUNT} child pages, got {len(filenames)}")

    canonical_urls = set()
    for filename in filenames:
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        canonical = re.search(r'<link rel="canonical" href="([^"]+)">', text)
        og_url = re.search(r'<meta property="og:url" content="([^"]+)">', text)
        expected_url = f"https://englishclass.kr/{filename}"
        if not canonical or canonical.group(1) != expected_url:
            raise ValueError(f"Invalid canonical URL in {filename}")
        if not og_url or og_url.group(1) != expected_url:
            raise ValueError(f"Invalid OG URL in {filename}")
        if '<div class="subdistricts">' in text or "전체 읍면동 보기</a>" not in text:
            raise ValueError(f"Invalid child navigation in {filename}")
        canonical_urls.add(canonical.group(1))

    if len(canonical_urls) != len(filenames):
        raise ValueError("Duplicate child canonical URLs found")

    for slug, (_, localities) in DISTRICTS.items():
        parent = ROOT / f"english-daegu-{slug}.html"
        text = parent.read_text(encoding="utf-8")
        links = re.findall(r'<a href="(english-daegu-[^"]+-\d+\.html)">', text)
        if len(links) != len(localities) or len(links) != len(set(links)):
            raise ValueError(f"Invalid child links in {parent.name}")
        if not all((ROOT / link).exists() for link in links):
            raise ValueError(f"Broken child link in {parent.name}")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap_urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    expected_urls = {f"https://englishclass.kr/{filename}" for filename in filenames}
    if sum(url in expected_urls for url in sitemap_urls) != len(expected_urls):
        raise ValueError("Missing or duplicate Daegu child sitemap entries")


def main() -> None:
    generated_files = []
    for slug, (district_name, localities) in DISTRICTS.items():
        source = update_parent(slug, district_name, localities)
        parent_filename = f"english-daegu-{slug}.html"
        expected = {
            f"english-daegu-{slug}-{index}.html"
            for index in range(1, len(localities) + 1)
        }
        for old in ROOT.glob(f"english-daegu-{slug}-*.html"):
            if old.name not in expected:
                old.unlink()
        for index, locality in enumerate(localities, 1):
            filename = f"english-daegu-{slug}-{index}.html"
            (ROOT / filename).write_text(
                child_from_parent(source, district_name, locality, filename, parent_filename),
                encoding="utf-8",
                newline="\n",
            )
            generated_files.append(filename)

    update_sitemap(generated_files)
    validate_output(generated_files)
    print(f"Updated {len(DISTRICTS)} Daegu parent pages")
    print(f"Generated {len(generated_files)} Daegu 읍면동 pages")
    print(f"Added {len(generated_files)} pages to sitemap.xml")
    print("Validated child metadata, parent links, and sitemap entries")


if __name__ == "__main__":
    main()