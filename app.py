from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import subprocess

app = Flask(__name__)

def get_all_prices_today():
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT code, price_etb, volume
        FROM prices
        WHERE date = (SELECT MAX(date) FROM prices)
        ORDER BY price_etb DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_price_history(code):
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, price_etb FROM prices
        WHERE code = ?
        ORDER BY date DESC LIMIT 30
    """, (code,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_latest_date():
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date) FROM prices")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

COFFEE_NAMES = {
    "LU": "Limu Unwashed",
    "LW": "Limu Washed",
    "RW": "Robusta Washed",
    "WW": "Wellega Washed",
    "WH": "Washed Harar",
    "GM": "Gimbi",
    "SB": "Sidama Buno",
}

def get_coffee_name(code):
    prefix = code[:2]
    grade = code[-1]
    name = COFFEE_NAMES.get(prefix, code)
    return f"{name} — Grade {grade}"

@app.route("/")
def home():
    today_prices = get_all_prices_today()
    latest_date = get_latest_date()
    jimma_history = get_price_history("LUBPAA2")
    enriched = [(code, get_coffee_name(code), price, volume) for code, price, volume in today_prices]
    return render_template("index.html",
        today_prices=enriched,
        latest_date=latest_date,
        jimma_history=jimma_history
    )

@app.route("/report", methods=["POST"])
def report():
    phone = request.form.get("phone")
    offered_price = request.form.get("offered_price")
    kebele = request.form.get("kebele")
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (phone, offered_price, kebele, date)
        VALUES (?, ?, ?, ?)
    """, (phone, float(offered_price), kebele, str(datetime.today().date())))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/run-daily-job")
def run_daily_job():
    subprocess.Popen(["python", "daily_job.py"])
    return "Daily job started!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)