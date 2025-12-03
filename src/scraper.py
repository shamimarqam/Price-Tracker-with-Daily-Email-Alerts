import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def clean_price(price_str: str):
    """
    Convert price string like '₹12,999' → 12999.
    """
    if not price_str:
        return None
    cleaned = "".join(ch for ch in price_str if ch.isdigit() or ch == ".")
    return float(cleaned) if cleaned else None


def fetch_page(url: str):
    """
    Fetch raw HTML content with retry and basic error handling.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None

# AMAZON SCRAPER
def get_amazon_price(url: str):
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Extract name
    title = soup.select_one("#productTitle")
    name = title.get_text(strip=True) if title else "Unknown Product"

    # Extract price (Amazon uses multiple price tags)
    price_tags = [
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "span.a-price-whole",
        "span.a-price > span.a-offscreen",  # fallback
    ]

    price = None
    for selector in price_tags:
        tag = soup.select_one(selector)
        if tag:
            price = clean_price(tag.get_text())
            if price:
                break

    return {
        "site": "amazon",
        "name": name,
        "price": price,
    }

# FLIPKART SCRAPER
def get_flipkart_price(url: str):
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Product name
    name_tag = soup.select_one("span.B_NuCI") or soup.select_one("span.LMizgS")
    name = name_tag.get_text(strip=True) if name_tag else "Unknown Product"

    # Price tag
    price_tag = soup.select_one("._30jeq3._16Jk6d") or soup.select_one(".hZ3P6w.bnqy13")
    '''
    .hZ3P6w.bnqy13
    span..LMizgS
    '''
    price = clean_price(price_tag.get_text()) if price_tag else None

    return {
        "site": "flipkart",
        "name": name,
        "price": price,
    }

# MYNTRA SCRAPER
def get_myntra_price(url: str):
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Product name
    name_tag = soup.select_one(".pdp-title, .pdp-name")
    name = name_tag.get_text(strip=True) if name_tag else "Unknown Product"

    # Price tag
    price_tag = soup.select_one(".pdp-price, .pdp-discount-container > .pdp-price")
    raw_price = price_tag.get_text() if price_tag else None
    price = clean_price(raw_price)

    return {
        "site": "myntra",
        "name": name,
        "price": price,
    }

# Unified function
def scrape_product(url: str):
    """
    Automatically detect website & delegate to correct scraper.
    """
    if "amazon" in url:
        return get_amazon_price(url)
    if "flipkart" in url:
        return get_flipkart_price(url)
    if "myntra" in url:
        return get_myntra_price(url)

    print(f"[ERROR] Unsupported URL: {url}")
    return None