"""
One-time scraper for the SHL Individual Test Solutions catalog.
Run: python scraper.py
Output: catalog.json
"""

import json
import time
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.shl.com"
CATALOG_URL = f"{BASE_URL}/products/product-catalog/"
OUTPUT_FILE = Path(__file__).parent / "catalog.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

TYPE_CODES = {"A", "B", "C", "D", "E", "K", "P", "S"}


def _get(session: requests.Session, url: str, retries: int = 3) -> requests.Response:
    for attempt in range(retries):
        try:
            resp = session.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            if attempt == retries - 1:
                raise
            print(f"  Retry {attempt + 1} for {url}: {exc}")
            time.sleep(2 ** attempt)


def _extract_types_from_row(row) -> list[str]:
    """Extract test type codes (A/B/C/D/E/K/P/S) from a table row."""
    types = []
    for cell in row.find_all("td"):
        # Look for cells that contain only type code letters
        text = cell.get_text(separator=" ", strip=True)
        # Match standalone uppercase letters that are valid type codes
        found = re.findall(r"\b([ABCDEKPS])\b", text)
        for f in found:
            if f in TYPE_CODES and f not in types:
                types.append(f)
    return types


def _extract_types_from_spans(row) -> list[str]:
    """Fallback: extract type codes from span elements."""
    types = []
    for span in row.find_all("span"):
        text = span.get_text(strip=True)
        if text in TYPE_CODES and text not in types:
            types.append(text)
    return types


def scrape_listing_page(session: requests.Session, start: int) -> list[dict]:
    """Scrape one page of the catalog listing, return Individual Test Solutions only."""
    url = f"{CATALOG_URL}?start={start}&type=1"
    resp = _get(session, url)
    soup = BeautifulSoup(resp.text, "html.parser")

    products = []

    # Find the "Individual Test Solutions" section
    individual_heading = None
    for tag in soup.find_all(["h2", "h3", "h4", "h5", "div"]):
        if "Individual Test Solutions" in tag.get_text():
            individual_heading = tag
            break

    if individual_heading is None:
        # Fallback: grab all product links on the page
        for a in soup.find_all("a", href=re.compile(r"/product-catalog/view/")):
            href = a["href"]
            name = a.get_text(strip=True)
            if not name:
                continue
            full_url = BASE_URL + href if href.startswith("/") else href
            row = a.find_parent("tr") or a.find_parent("li")
            types = _extract_types_from_row(row) if row else []
            if not types:
                types = _extract_types_from_spans(row) if row else []
            products.append({"name": name, "url": full_url, "test_types": types})
        return products

    # Find the table or list after the Individual Test Solutions heading
    table = individual_heading.find_next("table")
    if table:
        for row in table.find_all("tr"):
            a = row.find("a", href=re.compile(r"/product-catalog/view/"))
            if not a:
                continue
            name = a.get_text(strip=True)
            href = a["href"]
            full_url = BASE_URL + href if href.startswith("/") else href
            types = _extract_types_from_row(row)
            if not types:
                types = _extract_types_from_spans(row)
            products.append({"name": name, "url": full_url, "test_types": types})
    else:
        # No table found; search sibling elements for links
        current = individual_heading
        while current:
            current = current.find_next_sibling()
            if current is None:
                break
            # Stop if we hit another section heading
            if current.name in ("h2", "h3", "h4") and "Solutions" in current.get_text():
                break
            for a in current.find_all("a", href=re.compile(r"/product-catalog/view/")):
                name = a.get_text(strip=True)
                href = a["href"]
                full_url = BASE_URL + href if href.startswith("/") else href
                row = a.find_parent("tr") or a.find_parent("li")
                types = _extract_types_from_row(row) if row else []
                if not types:
                    types = _extract_types_from_spans(row) if row else []
                products.append({"name": name, "url": full_url, "test_types": types})

    return products


def scrape_detail_page(session: requests.Session, url: str) -> dict:
    """Scrape a product detail page for description and metadata."""
    try:
        resp = _get(session, url)
        soup = BeautifulSoup(resp.text, "html.parser")

        data: dict = {}

        # Description: try meta description first, then main content paragraphs
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.get("content"):
            data["description"] = meta_desc["content"].strip()[:400]
        else:
            # Find first substantial paragraph in main content
            for p in soup.find_all("p"):
                text = p.get_text(strip=True)
                if len(text) > 60:
                    data["description"] = text[:400]
                    break

        # Job levels
        levels = []
        for tag in soup.find_all(string=re.compile(
            r"(Director|Entry.Level|Executive|Graduate|Manager|"
            r"Mid.Professional|Front.Line|Supervisor|General Population)",
            re.IGNORECASE,
        )):
            word = tag.strip()
            if len(word) < 60 and word not in levels:
                levels.append(word)
        if levels:
            data["job_levels"] = levels[:10]

        # Remote testing
        page_text = soup.get_text(separator=" ", strip=True).lower()
        data["remote_testing"] = "remote" in page_text
        data["adaptive_irt"] = any(
            kw in page_text for kw in ("adaptive", "irt", "item response theory")
        )

        # Languages
        langs = []
        lang_section = soup.find(string=re.compile(r"language", re.IGNORECASE))
        if lang_section:
            parent = lang_section.find_parent()
            if parent:
                for sibling in parent.find_next_siblings()[:5]:
                    text = sibling.get_text(strip=True)
                    if len(text) < 60 and text:
                        langs.append(text)
        data["languages"] = langs[:10] if langs else None

        return data
    except Exception as exc:
        print(f"  Detail page error for {url}: {exc}")
        return {}


def scrape_all(fetch_details: bool = True) -> list[dict]:
    session = requests.Session()
    all_products: list[dict] = []
    seen_urls: set[str] = set()

    # Discover total pages from page 0
    resp = _get(session, f"{CATALOG_URL}?start=0&type=1")
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find pagination to determine total pages
    total_pages = 32  # Default fallback
    pager = soup.find(class_=re.compile(r"pager|pagination", re.IGNORECASE))
    if pager:
        page_links = pager.find_all("a")
        nums = [int(a.get_text(strip=True)) for a in page_links
                if a.get_text(strip=True).isdigit()]
        if nums:
            total_pages = max(nums)

    print(f"Scraping {total_pages} pages of Individual Test Solutions...")

    for page_num in range(total_pages):
        start = page_num * 12
        print(f"  Page {page_num + 1}/{total_pages} (start={start})", end="", flush=True)
        try:
            items = scrape_listing_page(session, start)
            new_items = [i for i in items if i["url"] not in seen_urls]
            for i in new_items:
                seen_urls.add(i["url"])
            all_products.extend(new_items)
            print(f" → {len(new_items)} items (total: {len(all_products)})")
        except Exception as exc:
            print(f" ERROR: {exc}")
        time.sleep(0.8)

    print(f"\nTotal unique products scraped: {len(all_products)}")

    if fetch_details:
        print("\nFetching detail pages for descriptions...")
        for i, product in enumerate(all_products):
            print(f"  [{i+1}/{len(all_products)}] {product['name'][:50]}", end="", flush=True)
            detail = scrape_detail_page(session, product["url"])
            product.update(detail)
            print(" ✓")
            time.sleep(0.5)

    return all_products


def main():
    fetch_details = "--no-details" not in sys.argv
    if not fetch_details:
        print("Skipping detail pages (--no-details flag set)")

    products = scrape_all(fetch_details=fetch_details)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(products)} products to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
