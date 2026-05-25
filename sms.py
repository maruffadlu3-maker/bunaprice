from twilio.rest import Client
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

def get_latest_price():
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price_etb, date FROM prices ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row

def send_sms(to_number, message):
    msg = client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )
    print(f"✅ SMS sent! ID: {msg.sid}")

def send_price_alert():
    row = get_latest_price()
    if not row:
        print("No price in database yet.")
        return
    
    price, date = row
    message = f"Buna Price: Jimma coffee today is {int(price)} ETB/Feresula ({date}). - BunaPrice"
    
    # Add farmer numbers here
    farmers = [
        "+251966880861",  # add more numbers below
        "+251948385444",
        "+251938612036",
        "+251917223102",
        "+251722030705",
        
        
    ]
    
    for number in farmers:
        send_sms(number, message)