from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent
SITE_URL = "https://englishclass.kr"
EXPECTED_PARENT_COUNT = 229

CSS = ".subdistricts{margin-top:24px;padding-top:20px;border-top:1px solid var(--line)}.subdistricts h2{margin:0 0 12px;font-size:19px}.subdistrict-links{display:flex;flex-wrap:wrap;gap:8px}.subdistrict-links a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:#2f3f61;font-size:13px;font-weight:700}"
CTA_MARKER = "    </div>\n  </div>\n</section>\n</main>"


def parent_pages() -> list[Path]:
    language_index = (ROOT / "japanese.html").read_text(encoding="utf-8")
    region_filenames = re.findall(
        r"class='region-card' href='(japanese-[^']+\.html)'",
        language_index,
    )
    parent_filenames = []
    for region_filename in region_filenames:
        region_text = (ROOT / region_filename).read_text(encoding="utf-8")
        parent_filenames.extend(
            re.findall(r"class='chip' href='(japanese-[^']+\.html)'", region_text)
        )
    pages = sorted(ROOT / filename for filename in parent_filenames)
    if len(pages) != EXPECTED_PARENT_COUNT:
        raise ValueError(f"Expected {EXPECTED_PARENT_COUNT} Japanese parent pages, got {len(pages)}")
    return pages


def page_details(path: Path) -> tuple[str, str, str]:
    match = re.fullmatch(r"japanese-([^-]+)-(.+)\.html", path.name)
    if not match:
        raise ValueError(f"Unexpected parent filename: {path.name}")
    region, district_slug = match.groups()
    text = path.read_text(encoding="utf-8")
    breadcrumb_nav = re.search(r'<nav class="bread".*?</nav>', text, flags=re.S)
    breadcrumbs = re.findall(r"<span>([^<]+)</span>", breadcrumb_nav.group(0)) if breadcrumb_nav else []
    if not breadcrumbs:
        raise ValueError(f"District breadcrumb not found in {path.name}")
    return region, district_slug, breadcrumbs[-1]


def locality_map() -> dict[Path, list[tuple[str, str]]]:
    mapping = {}
    for parent in parent_pages():
        english_parent = ROOT / parent.name.replace("japanese-", "english-", 1)
        if not english_parent.exists():
            raise ValueError(f"English locality source not found for {parent.name}")
        english_text = english_parent.read_text(encoding="utf-8")
        english_stem = re.escape(english_parent.stem)
        matches = re.findall(
            rf'<a href="{english_stem}-([^"]+)\.html">([^<]+)</a>',
            english_text,
        )
        suffixes = [suffix for suffix, _ in matches]
        if not matches or len(suffixes) != len(set(suffixes)):
            raise ValueError(f"Invalid English locality source in {english_parent.name}")
        if not all((ROOT / f"{english_parent.stem}-{suffix}.html").exists() for suffix in suffixes):
            raise ValueError(f"Broken English child source in {english_parent.name}")
        mapping[parent] = matches
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


def update_parent(path: Path, localities: list[tuple[str, str]]) -> str:
    region, district_slug, _ = page_details(path)
    source = remove_subdistricts(path.read_text(encoding="utf-8"))
    text = source
    if ".subdistricts{" not in text:
        text = text.replace(".photo-strip{", CSS + ".photo-strip{", 1)

    links = "\n".join(
        f'        <a href="japanese-{region}-{district_slug}-{suffix}.html">{locality}</a>'
        for suffix, locality in localities
    )
    heading = re.search(r"<h1>(.*?) 일본어회화</h1>", source)
    if not heading:
        raise ValueError(f"Parent heading not found in {path.name}")
    block = f'''    <div class="subdistricts">
      <h2>{heading.group(1)} 읍면동 일본어회화</h2>
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
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return source


def child_from_parent(
    source: str,
    region: str,
    district_slug: str,
    district_name: str,
    locality: str,
    filename: str,
) -> str:
    parent_filename = f"japanese-{region}-{district_slug}.html"
    heading = re.search(r"<h1>(.*?) 일본어회화</h1>", source)
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
        r'<a class="btn ghost" href="japanese-[^"]+\.html">[^<]+ 시·군·구 전체 보기</a>',
        f'<a class="btn ghost" href="{parent_filename}">{district_name} 전체 읍면동 보기</a>',
        text,
        count=1,
    )
    return text


def update_sitemap(filenames: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    child_url_prefixes = tuple(f"{SITE_URL}/{parent.stem}-" for parent in parent_pages())

    def remove_existing(match: re.Match) -> str:
        location = re.search(r"<loc>([^<]+)</loc>", match.group(0))
        return "" if location and location.group(1).startswith(child_url_prefixes) else match.group(0)

    text = re.sub(r"\s*<url>.*?</url>", remove_existing, text, flags=re.S)
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


def expected_filenames(mapping: dict[Path, list[tuple[str, str]]]) -> list[str]:
    filenames = []
    for parent, localities in mapping.items():
        region, district_slug, _ = page_details(parent)
        filenames.extend(
            f"japanese-{region}-{district_slug}-{suffix}.html"
            for suffix, _ in localities
        )
    return filenames


def validate_output(mapping: dict[Path, list[tuple[str, str]]], filenames: list[str]) -> None:
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
        if "일본어회화" not in text or "japanese.html" not in text:
            raise ValueError(f"Invalid Japanese content in {filename}")
        canonical_urls.add(canonical.group(1))
    if canonical_urls != expected_urls:
        raise ValueError("Duplicate or missing child canonical URLs")

    for parent, localities in mapping.items():
        region, district_slug, _ = page_details(parent)
        text = parent.read_text(encoding="utf-8")
        pattern = rf'<a href="(japanese-{region}-{re.escape(district_slug)}-[^"]+\.html)">'
        links = re.findall(pattern, text)
        if len(links) != len(localities) or len(links) != len(set(links)):
            raise ValueError(f"Invalid child links in {parent.name}")
        if not all((ROOT / link).exists() for link in links):
            raise ValueError(f"Broken child link in {parent.name}")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap_urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    child_url_prefixes = tuple(f"{SITE_URL}/{parent.stem}-" for parent in mapping)
    actual_child_urls = [
        url for url in sitemap_urls if url and url.startswith(child_url_prefixes)
    ]
    if len(actual_child_urls) != len(expected_urls) or set(actual_child_urls) != expected_urls:
        raise ValueError("Missing, duplicate, or orphaned child sitemap entries")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate source matching without writing files")
    parser.add_argument("--validate", action="store_true", help="Validate generated pages without writing files")
    args = parser.parse_args()

    mapping = locality_map()
    filenames = expected_filenames(mapping)
    if args.check:
        print(f"Matched {len(mapping)} parent pages to {len(filenames)} 읍면동")
        sample = ROOT / "japanese-seoul-jongno.html"
        print(f"Seoul Jongno-gu: {', '.join(locality for _, locality in mapping[sample])}")
        return
    if args.validate:
        validate_output(mapping, filenames)
        print(f"Validated {len(mapping)} parent pages and {len(filenames)} 읍면동 pages")
        return

    generated_files = []
    for parent, localities in mapping.items():
        region, district_slug, district_name = page_details(parent)
        source = update_parent(parent, localities)
        expected = {
            f"japanese-{region}-{district_slug}-{suffix}.html"
            for suffix, _ in localities
        }
        for old in ROOT.glob(f"japanese-{region}-{district_slug}-*.html"):
            if old.name not in expected:
                old.unlink()
        for suffix, locality in localities:
            filename = f"japanese-{region}-{district_slug}-{suffix}.html"
            text = child_from_parent(
                source,
                region,
                district_slug,
                district_name,
                locality,
                filename,
            )
            (ROOT / filename).write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
            generated_files.append(filename)

    update_sitemap(generated_files)
    validate_output(mapping, generated_files)
    print(f"Updated {len(mapping)} parent pages")
    print(f"Generated {len(generated_files)} 읍면동 pages")
    print(f"Added {len(generated_files)} pages to sitemap.xml")
    print("Validated Japanese metadata, parent links, child navigation, and sitemap entries")


if __name__ == "__main__":
    main()