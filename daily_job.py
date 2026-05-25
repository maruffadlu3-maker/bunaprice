from scraper import scrape_price
from sms import send_price_alert

print("=== Buna Price Daily Job Started ===")

# Step 1: Fetch today's price from ECX
scrape_price()

# Step 2: Send SMS to all farmers
send_price_alert()

print("=== Daily Job Complete ===")