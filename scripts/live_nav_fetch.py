"""
live_nav_fetch.py

Fetches live NAV data from the mfapi.in public API for HDFC Top 100 Direct
and 5 key schemes (SBI, ICICI, Nippon, Axis, Kotak Bluechip), parses the
JSON response, and saves each as a raw CSV in data/raw/.

Run from the project root:
    python scripts/live_nav_fetch.py
"""

import requests
import pandas as pd
import os

RAW_DATA_DIR = os.path.join("data", "raw")
BASE_URL = "https://api.mfapi.in/mf/{}"

SCHEMES = {
    125497: "hdfc_top100_direct",
    119551: "sbi_bluechip",
    120503: "icici_bluechip",
    118632: "nippon_large_cap",
    119092: "axis_bluechip",
    120841: "kotak_bluechip",
}


def fetch_nav(scheme_code: int) -> dict:
    """Fetch NAV JSON data for a given AMFI scheme code."""
    response = requests.get(BASE_URL.format(scheme_code), timeout=15)
    response.raise_for_status()
    return response.json()


def save_nav_as_csv(scheme_code: int, name: str, json_data: dict) -> None:
    """Parse the JSON response and save NAV history + meta info as CSV."""
    meta = json_data.get("meta", {})
    nav_history = json_data.get("data", [])

    if not nav_history:
        print(f"  WARNING: No NAV data found for {scheme_code} ({name})")
        return

    df = pd.DataFrame(nav_history)
    df["scheme_code"] = scheme_code
    df["scheme_name"] = meta.get("scheme_name", name)
    df["fund_house"] = meta.get("fund_house", "")
    df["scheme_category"] = meta.get("scheme_category", "")
    df["scheme_type"] = meta.get("scheme_type", "")

    df = df[["scheme_code", "scheme_name", "fund_house", "scheme_category",
              "scheme_type", "date", "nav"]]

    filepath = os.path.join(RAW_DATA_DIR, f"nav_{scheme_code}_{name}.csv")
    df.to_csv(filepath, index=False)
    print(f"  Saved {filepath}  |  {len(df)} NAV records")


def main() -> None:
    """Fetch and save live NAV data for all configured schemes."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    for scheme_code, name in SCHEMES.items():
        print(f"Fetching scheme {scheme_code} ({name}) ...")
        try:
            json_data = fetch_nav(scheme_code)
            save_nav_as_csv(scheme_code, name, json_data)
        except requests.exceptions.RequestException as e:
            print(f"  ERROR fetching {scheme_code}: {e}")

    print("Done. Check data/raw/ for saved CSV files.")


if __name__ == "__main__":
    main()
