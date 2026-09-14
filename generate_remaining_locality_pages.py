from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import re
import xml.etree.ElementTree as ET

try:
    import admdongkor as adk
except ImportError as error:
    raise SystemExit("Install the generator dependency with: python -m pip install admdongkor==0.7.0") from error


ROOT = Path(__file__).parent
DATA_VERSION = "20250401"
SITE_URL = "https://englishclass.kr"
EXPECTED_PARENT_COUNT = 138
EXPECTED_LOCALITY_COUNT = 2015

# Locality names come from SGIS data distributed by vuski/admdongkor under
# KOGL Type 1 and CC BY 4.0: https://github.com/vuski/admdongkor

REGIONS = {
    "chungbuk": "충청북도",
    "chungnam": "충청남도",
    "daejeon": "대전광역시",
    "gangwon": "강원특별자치도",
    "gwangju": "광주광역시",
    "gyeongbuk": "경상북도",
    "gyeongnam": "경상남도",
    "jeju": "제주특별자치도",
    "jeonbuk": "전북특별자치도",
    "jeonnam": "전라남도",
    "sejong": "세종특별자치시",
    "ulsan": "울산광역시",
}

CSS = ".subdistricts{margin-top:24px;padding-top:20px;border-top:1px solid var(--line)}.subdistricts h2{margin:0 0 12px;font-size:19px}.subdistrict-links{display:flex;flex-wrap:wrap;gap:8px}.subdistrict-links a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:#2f3f61;font-size:13px;font-weight:700}"
CTA_MARKER = "    </div>\n  </div>\n</section>\n</main>"


def parent_pages() -> list[Path]:
    pages = []
    for region in REGIONS:
        pages.extend(
            path
            for path in ROOT.glob(f"english-{region}-*.html")
            if not re.search(r"-\d+\.html$", path.name)
        )
    return sorted(pages)


def page_details(path: Path) -> tuple[str, str, str]:
    match = re.fullmatch(r"english-([^-]+)-(.+)\.html", path.name)
    if not match or match.group(1) not in REGIONS:
        raise ValueError(f"Unexpected parent filename: {path.name}")
    region, district_slug = match.groups()
    text = path.read_text(encoding="utf-8")
    breadcrumb_nav = re.search(r'<nav class="bread".*?</nav>', text, flags=re.S)
    breadcrumbs = re.findall(r"<span>([^<]+)</span>", breadcrumb_nav.group(0)) if breadcrumb_nav else []
    if not breadcrumbs:
        raise ValueError(f"District breadcrumb not found in {path.name}")
    return region, district_slug, breadcrumbs[-1]


def locality_map() -> dict[Path, list[str]]:
    data = adk.get(DATA_VERSION, "emd")
    mapping = {}
    for path in parent_pages():
        region, _, district_name = page_details(path)
        rows = data[data["sidonm"] == REGIONS[region]]
        if region == "sejong":
            matches = rows
        else:
            matches = rows[
                (rows["sggnm"] == district_name)
                | rows["sggnm"].fillna("").str.startswith(district_name)
            ]
        if matches.empty:
            raise ValueError(f"No administrative localities matched {path.name} ({district_name})")

        localities = []
        for row in matches.itertuples():
            prefix = ""
            if row.sggnm and row.sggnm != district_name:
                prefix = row.sggnm.removeprefix(district_name).strip() + " "
            locality = prefix + row.emdnm
            if locality not in localities:
                localities.append(locality)
        mapping[path] = localities
    if len(mapping) != EXPECTED_PARENT_COUNT:
        raise ValueError(f"Expected {EXPECTED_PARENT_COUNT} parent pages, got {len(mapping)}")
    locality_count = sum(len(localities) for localities in mapping.values())
    if locality_count != EXPECTED_LOCALITY_COUNT:
        raise ValueError(f"Expected {EXPECTED_LOCALITY_COUNT} localities, got {locality_count}")
    return mapping


def remove_subdistricts(text: str) -> str:
    text = text.replace(CSS, "", 1)
    return re.sub(
        r'\s*<div class="subdistricts">.*?</div>\s*</div>',
        "",
        text,
        count=1,
        flags=re.S,
    )


def update_parent(path: Path, localities: list[str]) -> str:
    region, district_slug, district_name = page_details(path)
    source = remove_subdistricts(path.read_text(encoding="utf-8"))
    text = source
    if ".subdistricts{" not in text:
        text = text.replace(".photo-strip{", CSS + ".photo-strip{", 1)

    links = "\n".join(
        f'        <a href="english-{region}-{district_slug}-{index}.html">{locality}</a>'
        for index, locality in enumerate(localities, 1)
    )
    heading = re.search(r"<h1>(.*?) 영어회화</h1>", source)
    if not heading:
        raise ValueError(f"Parent heading not found in {path.name}")
    block = f'''    <div class="subdistricts">
      <h2>{heading.group(1)} 읍면동 영어회화</h2>
      <div class="subdistrict-links">
{links}
      </div>
    </div>
'''
    if CTA_MARKER not in text:
        raise ValueError(f"CTA marker not found in {path.name}")
    text = text.replace(
        CTA_MARKER,
        "    </div>\n" + block + "  </div>\n</section>\n</main>",
        1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    return source


def child_from_parent(
    source: str,
    region: str,
    district_slug: str,
    district_name: str,
    locality: str,
    filename: str,
) -> str:
    parent_filename = f"english-{region}-{district_slug}.html"
    heading = re.search(r"<h1>(.*?) 영어회화</h1>", source)
    if not heading:
        raise ValueError(f"Parent heading not found for {filename}")
    parent_label = heading.group(1)
    child_label = f"{parent_label} {locality}"
    text = source.replace(parent_label, child_label)
    text = text.replace(
        f"{SITE_URL}/{parent_filename}",
        f"{SITE_URL}/{filename}",
    )
    text = text.replace(
        f"<span>{district_name}</span>",
        f'<a href="{parent_filename}">{district_name}</a>\n      <span>›</span>\n      <span>{locality}</span>',
        1,
    )
    text = re.sub(
        r'<a class="btn ghost" href="english-[^"]+\.html">[^<]+ 시·군·구 전체 보기</a>',
        f'<a class="btn ghost" href="{parent_filename}">{district_name} 전체 읍면동 보기</a>',
        text,
        count=1,
    )
    return text


def update_sitemap(filenames: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    region_pattern = "|".join(REGIONS)
    text = re.sub(
        rf'\s*<url>\s*<loc>{re.escape(SITE_URL)}/english-(?:{region_pattern})-[^<]+-\d+\.html</loc>.*?</url>',
        "",
        text,
        flags=re.S,
    )
    today = date.today().isoformat()
    entries = "\n".join(
        f'''  <url>
    <loc>{SITE_URL}/{filename}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>'''
        for filename in filenames
    )
    text = text.replace("</urlset>", entries + "\n</urlset>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate_output(mapping: dict[Path, list[str]], filenames: list[str]) -> None:
    expected_urls = {f"{SITE_URL}/{filename}" for filename in filenames}
    canonical_urls = set()
    for filename in filenames:
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        expected_url = f"{SITE_URL}/{filename}"
        canonical = re.search(r'<link rel="canonical" href="([^"]+)">', text)
        og_url = re.search(r'<meta property="og:url" content="([^"]+)">', text)
        if not canonical or canonical.group(1) != expected_url:
            raise ValueError(f"Invalid canonical URL in {filename}")
        if not og_url or og_url.group(1) != expected_url:
            raise ValueError(f"Invalid OG URL in {filename}")
        if '<div class="subdistricts">' in text or "전체 읍면동 보기</a>" not in text:
            raise ValueError(f"Invalid child navigation in {filename}")
        canonical_urls.add(canonical.group(1))
    if canonical_urls != expected_urls:
        raise ValueError("Duplicate or missing child canonical URLs")

    for parent, localities in mapping.items():
        region, district_slug, _ = page_details(parent)
        text = parent.read_text(encoding="utf-8")
        pattern = rf'<a href="(english-{region}-{re.escape(district_slug)}-\d+\.html)">'
        links = re.findall(pattern, text)
        if len(links) != len(localities) or len(links) != len(set(links)):
            raise ValueError(f"Invalid child links in {parent.name}")
        if not all((ROOT / link).exists() for link in links):
            raise ValueError(f"Broken child link in {parent.name}")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap_urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    if sum(url in expected_urls for url in sitemap_urls) != len(expected_urls):
        raise ValueError("Missing or duplicate child sitemap entries")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate data matching without writing files")
    parser.add_argument("--validate", action="store_true", help="Validate generated pages without writing files")
    args = parser.parse_args()

    mapping = locality_map()
    locality_count = sum(len(localities) for localities in mapping.values())
    if args.check:
        print(f"Matched {len(mapping)} parent pages to {locality_count} 읍면동")
        sample = ROOT / "english-daejeon-jung.html"
        print(f"Daejeon Jung-gu: {', '.join(mapping[sample])}")
        return
    if args.validate:
        filenames = []
        for parent, localities in mapping.items():
            region, district_slug, _ = page_details(parent)
            filenames.extend(
                f"english-{region}-{district_slug}-{index}.html"
                for index in range(1, len(localities) + 1)
            )
        validate_output(mapping, filenames)
        print(f"Validated {len(mapping)} parent pages and {len(filenames)} 읍면동 pages")
        return

    generated_files = []
    for parent, localities in mapping.items():
        region, district_slug, district_name = page_details(parent)
        source = update_parent(parent, localities)
        expected = {
            f"english-{region}-{district_slug}-{index}.html"
            for index in range(1, len(localities) + 1)
        }
        for old in ROOT.glob(f"english-{region}-{district_slug}-*.html"):
            if old.name not in expected:
                old.unlink()
        for index, locality in enumerate(localities, 1):
            filename = f"english-{region}-{district_slug}-{index}.html"
            text = child_from_parent(
                source,
                region,
                district_slug,
                district_name,
                locality,
                filename,
            )
            (ROOT / filename).write_text(text, encoding="utf-8", newline="\n")
            generated_files.append(filename)

    update_sitemap(generated_files)
    validate_output(mapping, generated_files)
    print(f"Updated {len(mapping)} parent pages")
    print(f"Generated {len(generated_files)} 읍면동 pages")
    print(f"Added {len(generated_files)} pages to sitemap.xml")
    print("Validated metadata, parent links, child navigation, and sitemap entries")


if __name__ == "__main__":
    main()