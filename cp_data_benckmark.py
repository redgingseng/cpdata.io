import requests
from datetime import datetime, timedelta
import csv
import os

def get_china_time():
    # 转换为北京时间
    return (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

def fetch_data(novel_id):
    url = f"https://www.gongzicp.com/webapi/novel/novelInfo?id={novel_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        res_json = r.json()
        
        if res_json.get("code") != 200:
            print(f"Error fetching ID {novel_id}: {res_json.get('msg')}")
            return None
            
        data = res_json["data"]
        
        return {
            "time": get_china_time(),
            "novel_id": novel_id,
            "novel_name": data.get("novel_name", "Unknown"),
            "allpopu_wan": round(data["novel_allpopu"] / 10000, 2), # 保留两位小数
            "read_total": data["read_total"],
        }
    except Exception as e:
        print(f"Request failed for {novel_id}: {e}")
        return None

def main():
    # 需要监控的 ID 列表
    target_ids = ["1606051", "2043165", "1736008", "1633197", "1499282"]
    file_name = "data.csv"
    
    results = []
    for nid in target_ids:
        info = fetch_data(nid)
        if info:
            results.append(info)
    
    if not results:
        print("No data collected.")
        return

    file_exists = os.path.exists(file_name)
    # 定义表头
    fieldnames = ["time", "novel_id", "novel_name", "allpopu_wan", "read_total"]

    with open(file_name, "a", newline="", encoding="utf-8-sig") as f: # 使用 utf-8-sig 让 Excel 打开不乱码
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)
    
    print(f"Successfully updated {len(results)} rows at {get_china_time()}")

if __name__ == "__main__":
    main()
