from datetime import date
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent

# Administrative 읍면동 names for the 10 Incheon districts and counties.
DISTRICTS = {
    "jung": ("중구", [
        "신포동", "연안동", "신흥동", "도원동", "율목동", "동인천동", "개항동",
        "영종동", "영종1동", "영종2동", "운서동", "용유동",
    ]),
    "dong": ("동구", [
        "만석동", "화수1·화평동", "화수2동", "송현1·2동", "송현3동", "송림1동",
        "송림2동", "송림3·5동", "송림4동", "송림6동", "금창동",
    ]),
    "michuhol": ("미추홀구", [
        "숭의1·3동", "숭의2동", "숭의4동", "용현1·4동", "용현2동", "용현3동",
        "용현5동", "학익1동", "학익2동", "도화1동", "도화2·3동", "주안1동",
        "주안2동", "주안3동", "주안4동", "주안5동", "주안6동", "주안7동",
        "주안8동", "관교동", "문학동",
    ]),
    "yeonsu": ("연수구", [
        "옥련1동", "옥련2동", "선학동", "연수1동", "연수2동", "연수3동", "청학동",
        "동춘1동", "동춘2동", "동춘3동", "송도1동", "송도2동", "송도3동", "송도4동", "송도5동",
    ]),
    "namdong": ("남동구", [
        "구월1동", "구월2동", "구월3동", "구월4동", "간석1동", "간석2동", "간석3동", "간석4동",
        "만수1동", "만수2동", "만수3동", "만수4동", "만수5동", "만수6동", "장수서창동", "서창2동",
        "남촌도림동", "논현1동", "논현2동", "논현고잔동",
    ]),
    "bupyeong": ("부평구", [
        "부평1동", "부평2동", "부평3동", "부평4동", "부평5동", "부평6동", "산곡1동", "산곡2동",
        "산곡3동", "산곡4동", "청천1동", "청천2동", "갈산1동", "갈산2동", "삼산1동", "삼산2동",
        "부개1동", "부개2동", "부개3동", "일신동", "십정1동", "십정2동",
    ]),
    "gyeyang": ("계양구", [
        "효성1동", "효성2동", "계산1동", "계산2동", "계산3동", "계산4동", "작전1동", "작전2동",
        "작전서운동", "계양1동", "계양2동", "계양3동",
    ]),
    "seo": ("서구", [
        "검암경서동", "연희동", "청라1동", "청라2동", "청라3동", "가정1동", "가정2동", "가정3동",
        "신현원창동", "석남1동", "석남2동", "석남3동", "가좌1동", "가좌2동", "가좌3동", "가좌4동",
        "검단동", "불로대곡동", "원당동", "당하동", "오류왕길동", "마전동", "아라동",
    ]),
    "ganghwa": ("강화군", [
        "강화읍", "선원면", "불은면", "길상면", "화도면", "양도면", "내가면", "하점면",
        "양사면", "송해면", "교동면", "삼산면", "서도면",
    ]),
    "ongjin": ("옹진군", [
        "북도면", "백령면", "대청면", "덕적면", "영흥면", "자월면", "연평면",
    ]),
}

CSS = ".subdistricts{margin-top:24px;padding-top:20px;border-top:1px solid var(--line)}.subdistricts h2{margin:0 0 12px;font-size:19px}.subdistrict-links{display:flex;flex-wrap:wrap;gap:8px}.subdistrict-links a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:#2f3f61;font-size:13px;font-weight:700}"


def remove_subdistricts(text: str) -> str:
    text = text.replace(CSS, "", 1)
    return re.sub(r'\n?\s*<div class="subdistricts">.*?</div>\s*</div>', "", text, count=1, flags=re.S)


def child_from_parent(source: str, district_name: str, locality: str, filename: str, parent_filename: str) -> str:
    text = remove_subdistricts(source)
    parent_label = f"인천 {district_name}"
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
        '<a class="btn ghost" href="english-incheon.html">인천 시·군·구 전체 보기</a>',
        f'<a class="btn ghost" href="{parent_filename}">{district_name} 전체 읍면동 보기</a>',
        1,
    )
    return text


def update_parent(slug: str, district_name: str, localities: list[str]) -> str:
    parent = ROOT / f"english-incheon-{slug}.html"
    if not parent.exists():
        raise FileNotFoundError(parent)

    source = parent.read_text(encoding="utf-8")
    text = source
    if ".subdistricts{" not in text:
        text = text.replace(".photo-strip{", CSS + ".photo-strip{", 1)

    links = "\n".join(
        f'        <a href="english-incheon-{slug}-{index}.html">{locality}</a>'
        for index, locality in enumerate(localities, 1)
    )
    block = f'''    <div class="subdistricts">
      <h2>인천 {district_name} 읍면동 영어회화</h2>
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
        r'\s*<url>\s*<loc>https://englishclass\.kr/english-incheon-[^<]+-\d+\.html</loc>.*?</url>',
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
    if len(filenames) != 156:
        raise ValueError(f"Expected 156 child pages, got {len(filenames)}")

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
        parent = ROOT / f"english-incheon-{slug}.html"
        text = parent.read_text(encoding="utf-8")
        links = re.findall(r'<a href="(english-incheon-[^"]+-\d+\.html)">', text)
        if len(links) != len(localities) or len(links) != len(set(links)):
            raise ValueError(f"Invalid child links in {parent.name}")
        if not all((ROOT / link).exists() for link in links):
            raise ValueError(f"Broken child link in {parent.name}")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap_urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    expected_urls = {f"https://englishclass.kr/{filename}" for filename in filenames}
    if sum(url in expected_urls for url in sitemap_urls) != len(expected_urls):
        raise ValueError("Missing or duplicate Incheon child sitemap entries")


def main() -> None:
    generated_files = []
    for slug, (district_name, localities) in DISTRICTS.items():
        source = update_parent(slug, district_name, localities)
        parent_filename = f"english-incheon-{slug}.html"
        expected = {
            f"english-incheon-{slug}-{index}.html"
            for index in range(1, len(localities) + 1)
        }
        for old in ROOT.glob(f"english-incheon-{slug}-*.html"):
            if old.name not in expected:
                old.unlink()
        for index, locality in enumerate(localities, 1):
            filename = f"english-incheon-{slug}-{index}.html"
            (ROOT / filename).write_text(
                child_from_parent(source, district_name, locality, filename, parent_filename),
                encoding="utf-8",
                newline="\n",
            )
            generated_files.append(filename)

    update_sitemap(generated_files)
    validate_output(generated_files)
    print(f"Updated {len(DISTRICTS)} Incheon parent pages")
    print(f"Generated {len(generated_files)} Incheon 읍면동 pages")
    print(f"Added {len(generated_files)} pages to sitemap.xml")
    print("Validated child metadata, parent links, and sitemap entries")


if __name__ == "__main__":
    main()
