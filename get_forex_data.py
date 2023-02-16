import os
import sys
import json
import datetime
import sqlite3
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY", "default")

try:
    resp = requests.get(
        "https://api.apilayer.com/exchangerates_data/timeseries?start_date=2023-01-15&end_date=2023-02-13&base=USD&symbols=EUR,GBP,JPY,AUD,CAD,INR,CHF",
        headers={"apikey": API_KEY},
    )
    resp.raise_for_status()
    if resp.status_code == 200:
        data = json.loads(resp.content)
        with open("data.json", "w") as f:
            json.dump(data, f)
except requests.exceptions.RequestException as e:
    print("API call failed", e)
    sys.exit()

with open("data.json", "r") as f:
    data = json.load(f)
    db_input = []
    if data["base"] == "USD":
        for k, v in data["rates"].items():
            db_input.append(
                (
                    k,
                    1,
                    v["EUR"],
                    v["GBP"],
                    v["JPY"],
                    v["AUD"],
                    v["CAD"],
                    v["INR"],
                    v["CHF"],
                )
            )

conn = sqlite3.connect("forex.db")
cursor = conn.cursor()
try:
    cursor.executemany(
        "insert into exchange_rates values (?,?,?,?,?,?,?,?,?)",
        db_input,
    )
    conn.commit()
    conn.close()
except Exception as e:
    print("Error.......")
    print(e)
    cursor.close()
    conn.rollback()
