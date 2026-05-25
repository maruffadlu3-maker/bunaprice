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
    message = f"Buna Price Update: Jimma coffee today is {price} ETB per Feresula (Date: {date}). - BunaPrice"
    
    # Put YOUR real phone number here with country code
    # Ethiopia code is +251
    # Example: +251912345678
    your_number = "+251966880861"
    
    send_sms(your_number, message)

send_price_alert()