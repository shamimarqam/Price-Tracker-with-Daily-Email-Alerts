#!/usr/bin/env python3

from tracker import track_prices
from emailer import send_email
from config import VERBOSE


def run():
    if VERBOSE:
        print("[INFO] Starting price tracking...")

    summary, drops = track_prices()

    if VERBOSE:
        print("[INFO] Tracking completed.")
        print(f"[INFO] Items tracked: {len(summary)}")
        print(f"[INFO] Price drops: {len(drops)}")

    send_email(summary, drops)

    if VERBOSE:
        print("[INFO] Daily email sent.")


if __name__ == "__main__":
    run()