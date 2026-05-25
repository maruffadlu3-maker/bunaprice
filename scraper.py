import requests
from bs4 import BeautifulSoup
from datetime import date
import sqlite3
import re

def save_price(price, grade):
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prices (date, price_etb)
        VALUES (?, ?)
    """, (str(date.today()), price))
    conn.commit()
    conn.close()
    print(f"✅ Saved: {grade} = {price} ETB on {date.today()}")

def scrape_price():
    print("Fetching today's Jimma coffee price from ECX...")

    url = "https://www.ecx.com.et/Pages/MarketDataPage.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Find all LWJM prices (Limu Washed Jimma)
        matches = re.findall(r'(LWJM\w*)\s+([\d,]+)\s*:', text)

        if matches:
            print("\n=== Today's Jimma Coffee Prices ===")
            for grade, price_str in matches:
                price = float(price_str.replace(",", ""))
                print(f"  {grade}: {price} ETB/Feresula")
                save_price(price, grade)
        else:
            print("No Jimma prices found today. Market may be closed.")

    except Exception as e:
        print(f"Error: {e}")

scrape_price()