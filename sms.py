import africastalking
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

username = os.getenv("AT_USERNAME")
api_key = os.getenv("AT_API_KEY")

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def get_latest_price():
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price_etb, date FROM prices ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row

def send_sms(to_number, message):
    response = sms.send(message, [to_number])
    print(f"✅ SMS sent to {to_number}! Response: {response}")

def send_price_alert():
    row = get_latest_price()
    if not row:
        print("No price in database yet.")
        return
    
    price, date = row
    message = f"Buna Price: Jimma coffee today is {int(price)} ETB/Feresula ({date}). - BunaPrice"
    
    farmers = [
        "+251966880861",
        "+251722030705",
    ]
    
    for number in farmers:
        send_sms(number, message)

