import requests
import json
from datetime import datetime, timedelta
import csv
import os

def get_china_time():
    return (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

def fetch_data():
    url = "https://www.gongzicp.com/webapi/novel/novelInfo?id=1952181"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()["data"]

    allpopu = data["novel_allpopu"] / 1e4
    read_total = data["read_total"]

    return {
        "time": get_china_time(),
        "allpopu_wan": allpopu,
        "read_total": read_total,
    }

def main():
    row = fetch_data()
    file_exists = os.path.exists("data.csv")

    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["time", "allpopu_wan", "read_total"]
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

if __name__ == "__main__":
    main()
