"""Keep neighborhood (dong) pages out of search indexes.

The dong pages repeat the district template with only the neighborhood name
changed, so they are marked noindex,follow and left out of sitemap.xml. That
lets search engines spend crawl and ranking signals on the home, language,
region, district, exam, and business pages instead. Run this again after any
generate_*.py script rewrites dong pages or sitemap.xml.
"""
from argparse import ArgumentParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent
SITE_URL = "https://englishclass.kr"
# Most dong pages end in a number; the Jongno set is named after each dong.
DONG_PAGE = re.compile(r"^(?:english|chinese|japanese)-(?:.+-\d+|seoul-jongno-.+)\.html$")
INDEX_ROBOTS = '<meta name="robots" content="index,follow,max-image-preview:large">'
NOINDEX_ROBOTS = '<meta name="robots" content="noindex,follow">'


def dong_pages() -> list[Path]:
    return sorted(path for path in ROOT.glob("*.html") if DONG_PAGE.match(path.name))


def apply_noindex(pages: list[Path]) -> int:
    changed = 0
    for path in pages:
        text = path.read_text(encoding="utf-8-sig")
        if NOINDEX_ROBOTS in text:
            continue
        if INDEX_ROBOTS not in text:
            raise ValueError(f"Robots meta tag not found in {path.name}")
        path.write_text(text.replace(INDEX_ROBOTS, NOINDEX_ROBOTS, 1), encoding="utf-8", newline="\n")
        changed += 1
    return changed


def prune_sitemap() -> int:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8-sig")
    removed = 0

    def drop_dong(match: re.Match) -> str:
        nonlocal removed
        if DONG_PAGE.match(match.group(1)):
            removed += 1
            return ""
        return match.group(0)

    text = re.sub(
        rf"\s*<url>\s*<loc>{re.escape(SITE_URL)}/([^<]*)</loc>.*?</url>",
        drop_dong,
        text,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    return removed


def validate(pages: list[Path]) -> None:
    for path in pages:
        if NOINDEX_ROBOTS not in path.read_text(encoding="utf-8-sig"):
            raise ValueError(f"{path.name} is still indexable")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [node.text for node in ET.parse(ROOT / "sitemap.xml").findall(f".//{namespace}loc")]
    leftovers = [url for url in urls if DONG_PAGE.match(url.rsplit("/", 1)[-1])]
    if leftovers:
        raise ValueError(f"Dong pages still in sitemap.xml: {leftovers[:3]}")
    missing = [url for url in urls if url != f"{SITE_URL}/" and not (ROOT / url.rsplit("/", 1)[-1]).exists()]
    if missing:
        raise ValueError(f"Sitemap URLs without a page: {missing[:3]}")
    if len(urls) != len(set(urls)):
        raise ValueError("Duplicate sitemap URLs")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--validate", action="store_true", help="Validate without writing files")
    args = parser.parse_args()

    pages = dong_pages()
    if not args.validate:
        print(f"Marked {apply_noindex(pages)} of {len(pages)} dong pages noindex")
        print(f"Removed {prune_sitemap()} dong URLs from sitemap.xml")
    validate(pages)
    print("Validated dong pages and sitemap.xml")


if __name__ == "__main__":
    main()
