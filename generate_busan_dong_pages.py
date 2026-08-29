from datetime import date
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent

# Administrative 읍면동 names for Busan's 16 districts and county.
DISTRICTS = {
    "jung": ("중구", [
        "중앙동", "동광동", "대청동", "보수동", "부평동", "광복동", "남포동", "영주1동", "영주2동",
    ]),
    "seo": ("서구", [
        "동대신1동", "동대신2동", "동대신3동", "서대신1동", "서대신3동", "서대신4동", "부민동",
        "아미동", "초장동", "충무동", "남부민1동", "남부민2동", "암남동",
    ]),
    "dong": ("동구", [
        "초량1동", "초량2동", "초량3동", "초량6동", "수정1동", "수정2동", "수정4동", "수정5동",
        "좌천동", "범일1동", "범일2동", "범일5동",
    ]),
    "yeongdo": ("영도구", [
        "남항동", "영선1동", "영선2동", "신선동", "봉래1동", "봉래2동", "청학1동", "청학2동",
        "동삼1동", "동삼2동", "동삼3동",
    ]),
    "busanjin": ("부산진구", [
        "부전1동", "부전2동", "연지동", "초읍동", "양정1동", "양정2동", "전포1동", "전포2동",
        "부암1동", "부암3동", "당감1동", "당감2동", "당감4동", "가야1동", "가야2동", "개금1동",
        "개금2동", "개금3동", "범천1동", "범천2동",
    ]),
    "dongnae": ("동래구", [
        "수민동", "복산동", "명륜동", "온천1동", "온천2동", "온천3동", "사직1동", "사직2동",
        "사직3동", "안락1동", "안락2동", "명장1동", "명장2동",
    ]),
    "nam": ("남구", [
        "대연1동", "대연3동", "대연4동", "대연5동", "대연6동", "용호1동", "용호2동", "용호3동",
        "용호4동", "용당동", "감만1동", "감만2동", "우암동", "문현1동", "문현2동", "문현3동", "문현4동",
    ]),
    "buk": ("북구", [
        "구포1동", "구포2동", "구포3동", "금곡동", "화명1동", "화명2동", "화명3동", "덕천1동",
        "덕천2동", "덕천3동", "만덕1동", "만덕2동", "만덕3동",
    ]),
    "haeundae": ("해운대구", [
        "우1동", "우2동", "우3동", "중1동", "중2동", "좌1동", "좌2동", "좌3동", "좌4동", "송정동",
        "반여1동", "반여2동", "반여3동", "반여4동", "반송1동", "반송2동", "재송1동", "재송2동",
    ]),
    "saha": ("사하구", [
        "괴정1동", "괴정2동", "괴정3동", "괴정4동", "당리동", "하단1동", "하단2동", "신평1동",
        "신평2동", "장림1동", "장림2동", "다대1동", "다대2동", "구평동", "감천1동", "감천2동",
    ]),
    "geumjeong": ("금정구", [
        "서1동", "서2동", "서3동", "금사회동동", "부곡1동", "부곡2동", "부곡3동", "부곡4동",
        "장전1동", "장전2동", "선두구동", "청룡노포동", "남산동", "구서1동", "구서2동", "금성동",
    ]),
    "gangseo": ("강서구", [
        "대저1동", "대저2동", "강동동", "명지1동", "명지2동", "가락동", "녹산동", "가덕도동",
    ]),
    "yeonje": ("연제구", [
        "거제1동", "거제2동", "거제3동", "거제4동", "연산1동", "연산2동", "연산3동", "연산4동",
        "연산5동", "연산6동", "연산8동", "연산9동",
    ]),
    "suyeong": ("수영구", [
        "남천1동", "남천2동", "수영동", "망미1동", "망미2동", "광안1동", "광안2동", "광안3동",
        "광안4동", "민락동",
    ]),
    "sasang": ("사상구", [
        "삼락동", "모라1동", "모라3동", "덕포1동", "덕포2동", "괘법동", "감전동", "주례1동",
        "주례2동", "주례3동", "학장동", "엄궁동",
    ]),
    "gijang": ("기장군", [
        "기장읍", "장안읍", "정관읍", "일광읍", "철마면",
    ]),
}

EXPECTED_PAGE_COUNT = 205
CSS = ".subdistricts{margin-top:24px;padding-top:20px;border-top:1px solid var(--line)}.subdistricts h2{margin:0 0 12px;font-size:19px}.subdistrict-links{display:flex;flex-wrap:wrap;gap:8px}.subdistrict-links a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:#2f3f61;font-size:13px;font-weight:700}"


def remove_subdistricts(text: str) -> str:
    text = text.replace(CSS, "", 1)
    return re.sub(r'\n?\s*<div class="subdistricts">.*?</div>\s*</div>', "", text, count=1, flags=re.S)


def child_from_parent(source: str, district_name: str, locality: str, filename: str, parent_filename: str) -> str:
    text = remove_subdistricts(source)
    parent_label = f"부산 {district_name}"
    label = f"{parent_label} {locality}"
    text = text.replace(parent_label, label)
    text = text.replace(
        f"https://englishclass.kr/{parent_filename}",
        f"https://englishclass.kr/{filename}",
    )
    text = text.replace(
        f"<span>{district_name}</span>",
        f'<a href="{parent_filename}">{district_name}</a>\n      <span>›</span>\n      <span>{locality}</span>',
        1,
    )
    text = text.replace(
        '<a class="btn ghost" href="english-busan.html">부산 시·군·구 전체 보기</a>',
        f'<a class="btn ghost" href="{parent_filename}">{district_name} 전체 읍면동 보기</a>',
        1,
    )
    return text


def update_parent(slug: str, district_name: str, localities: list[str]) -> str:
    parent = ROOT / f"english-busan-{slug}.html"
    if not parent.exists():
        raise FileNotFoundError(parent)

    source = parent.read_text(encoding="utf-8")
    text = source
    if ".subdistricts{" not in text:
        text = text.replace(".photo-strip{", CSS + ".photo-strip{", 1)

    links = "\n".join(
        f'        <a href="english-busan-{slug}-{index}.html">{locality}</a>'
        for index, locality in enumerate(localities, 1)
    )
    block = f'''    <div class="subdistricts">
      <h2>부산 {district_name} 읍면동 영어회화</h2>
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
        r'\s*<url>\s*<loc>https://englishclass\.kr/english-busan-[^<]+-\d+\.html</loc>.*?</url>',
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
        parent = ROOT / f"english-busan-{slug}.html"
        text = parent.read_text(encoding="utf-8")
        links = re.findall(r'<a href="(english-busan-[^"]+-\d+\.html)">', text)
        if len(links) != len(localities) or len(links) != len(set(links)):
            raise ValueError(f"Invalid child links in {parent.name}")
        if not all((ROOT / link).exists() for link in links):
            raise ValueError(f"Broken child link in {parent.name}")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap_urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    expected_urls = {f"https://englishclass.kr/{filename}" for filename in filenames}
    if sum(url in expected_urls for url in sitemap_urls) != len(expected_urls):
        raise ValueError("Missing or duplicate Busan child sitemap entries")


def main() -> None:
    generated_files = []
    for slug, (district_name, localities) in DISTRICTS.items():
        source = update_parent(slug, district_name, localities)
        parent_filename = f"english-busan-{slug}.html"
        expected = {
            f"english-busan-{slug}-{index}.html"
            for index in range(1, len(localities) + 1)
        }
        for old in ROOT.glob(f"english-busan-{slug}-*.html"):
            if old.name not in expected:
                old.unlink()
        for index, locality in enumerate(localities, 1):
            filename = f"english-busan-{slug}-{index}.html"
            (ROOT / filename).write_text(
                child_from_parent(source, district_name, locality, filename, parent_filename),
                encoding="utf-8",
                newline="\n",
            )
            generated_files.append(filename)

    update_sitemap(generated_files)
    validate_output(generated_files)
    print(f"Updated {len(DISTRICTS)} Busan parent pages")
    print(f"Generated {len(generated_files)} Busan 읍면동 pages")
    print(f"Added {len(generated_files)} pages to sitemap.xml")
    print("Validated child metadata, parent links, and sitemap entries")


if __name__ == "__main__":
    main()