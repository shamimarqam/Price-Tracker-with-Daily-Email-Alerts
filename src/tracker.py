import os
import pandas as pd
from datetime import datetime
from scraper import scrape_product
from utils import get_product_id
from config import PRODUCT_URLS, PRICE_HISTORY_CSV


def load_price_history():
    """Load existing CSV or create a new empty DataFrame."""
    if os.path.exists(PRICE_HISTORY_CSV):
        return pd.read_csv(PRICE_HISTORY_CSV)
    
    # Create new CSV structure
    df = pd.DataFrame(columns=[
        "product_id",
        "product_name",
        "site",
        "date",
        "price"
    ])
    df.to_csv(PRICE_HISTORY_CSV, index=False)
    return df


def append_price_entry(df, entry):
    """Append a price entry to the DataFrame."""
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    return df


def get_yesterday_price(df, product_id):
    """Fetch the last recorded price for a product."""
    product_rows = df[df["product_id"] == product_id]
    if len(product_rows) < 1:
        return None
    
    latest_row = product_rows.sort_values("date").iloc[-1]
    return latest_row["price"]


def track_prices():
    """Main function to track prices and log changes."""
    df = load_price_history()
    today = datetime.now().strftime("%Y-%m-%d")

    summary = []
    price_drops = []

    for url in PRODUCT_URLS:
        data = scrape_product(url)
        if not data or data["price"] is None:
            print(f"[WARNING] Could not scrape price for {url}")
            continue

        product_id = get_product_id(url)
        yesterday_price = get_yesterday_price(df, product_id)

        entry = {
            "product_id": product_id,
            "product_name": data["name"],
            "site": data["site"],
            "date": today,
            "price": data["price"],
        }

        df = append_price_entry(df, entry)
        summary.append(entry)

        if yesterday_price and data["price"] < yesterday_price:
            drop_info = {
                "product_name": data["name"],
                "site": data["site"],
                "old_price": yesterday_price,
                "new_price": data["price"],
                "url": url
            }
            price_drops.append(drop_info)

    # Save updated CSV
    df.to_csv(PRICE_HISTORY_CSV, index=False)

    return summary, price_drops


if __name__ == "__main__":
    summary, drops = track_prices()

    print("=== Today's Tracking Summary ===")
    for item in summary:
        print(f"{item['product_name']} ({item['site']}) → ₹{item['price']}")

    if drops:
        print("\n=== PRICE DROP ALERTS ===")
        for d in drops:
            print(f"{d['product_name']} dropped from ₹{d['old_price']} to ₹{d['new_price']}")