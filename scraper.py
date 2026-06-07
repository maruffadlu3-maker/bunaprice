import requests
from bs4 import BeautifulSoup
from datetime import date
import sqlite3
import re

COFFEE_NAMES = {
    "LU": "Limu Unwashed",
    "LW": "Limu Washed",
    "RW": "Robusta Washed",
    "WW": "Wellega Washed",
    "WH": "Washed Harar",
    "GM": "Gimbi",
    "SB": "Sidama Buno",
    "RU": "Robusta Unwashed",
    "GU": "Gimbi Unwashed",
}

def get_coffee_name(code):
    prefix = code[:2]
    grade = code[-1]
    name = COFFEE_NAMES.get(prefix, code)
    return f"{name} — Grade {grade}"

def save_price(code, price, volume):
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prices (date, code, price_etb, volume)
        VALUES (?, ?, ?, ?)
    """, (str(date.today()), code, price, volume))
    conn.commit()
    conn.close()

def scrape_price():
    print("Fetching today's coffee prices from ECX...")

    url = "https://www.ecx.com.et/Pages/MarketDataPage.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        matches = re.findall(r'([A-Z]{2,6}\d)\s+([\d,]+)\s*:\s*([\d,]*)', text)

        coffee_codes = ["LU", "LW", "RW", "WW", "WH", "GM", "SB"]
        found = False

        best_prices = {}
        for code, price_str, volume_str in matches:
            prefix = code[:2]
            if prefix in coffee_codes:
                price = float(price_str.replace(",", ""))
                volume = float(volume_str.replace(",", "")) if volume_str else 0
                if price > 1000 and volume > 0:
                    if code not in best_prices or price > best_prices[code][0]:
                        best_prices[code] = (price, volume)

        if best_prices:
            print("\n=== Today's ECX Coffee Prices ===")
            for code, (price, volume) in best_prices.items():
                name = get_coffee_name(code)
                print(f"  {code} ({name}): {price:,.0f} ETB | Volume: {volume:,.0f}")
                save_price(code, price, volume)
                found = True

        if not found:
            print("No coffee prices found today. Market may be closed.")

    except Exception as e:
        print(f"Error: {e}")

scrape_price()