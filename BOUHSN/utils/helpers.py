import datetime
import random
import csv
import os

# --------------------
# 今日の豆知識
# --------------------
def get_today_tip(tips):
    today = datetime.date.today()
    random.seed(today.toordinal())
    return random.choice(tips)

# --------------------
# 文字列切り詰め
# --------------------
def truncate_text(text, length=15):
    if len(text) <= length:
        return text
    return text[:length] + "…"

# --------------------
# CSV読み書き
# --------------------
def read_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(file_path, rows):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = rows[0].keys() if rows else ["date","key","checked","memo"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
