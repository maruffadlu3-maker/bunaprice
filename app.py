from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_prices():
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, price_etb FROM prices ORDER BY id DESC LIMIT 30")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_latest_price():
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, price_etb FROM prices ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row

@app.route("/")
def home():
    latest = get_latest_price()
    prices = get_prices()
    return render_template("index.html", latest=latest, prices=prices)

@app.route("/report", methods=["POST"])
def report():
    phone = request.form.get("phone")
    offered_price = request.form.get("offered_price")
    kebele = request.form.get("kebele")
    
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            offered_price REAL,
            kebele TEXT,
            date TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO reports (phone, offered_price, kebele, date)
        VALUES (?, ?, ?, ?)
    """, (phone, float(offered_price), kebele, str(datetime.today().date())))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

    @app.route("/run-daily-job")
def run_daily_job():
    import subprocess
    subprocess.Popen(["python", "daily_job.py"])
    return "Daily job started!", 200