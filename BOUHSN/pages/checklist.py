import streamlit as st
import datetime
import csv
import os

CHECKLIST_FILE = "data/checklist.csv"

ITEMS = [
    "鍵を閉めた",
    "不審なメールを開かなかった",
    "夜道で周囲を警戒した",
    "SNSで位置情報を投稿していない"
]

def render():
    st.markdown("## 防犯チェックリスト")

    today = datetime.date.today().isoformat()

    # --------------------
    # session_state 初期化
    # --------------------
    if "checklist" not in st.session_state:
        st.session_state.checklist = {}

    if today not in st.session_state.checklist:
        st.session_state.checklist[today] = {
            "checks": {item: False for item in ITEMS},
            "memo": ""
        }

    # ← これが超重要（data 未定義防止）
    data = st.session_state.checklist[today]

    # --------------------
    # チェック項目
    # --------------------
    st.markdown("### ✅ 今日のチェック")
    for item in ITEMS:
        data["checks"][item] = st.checkbox(
            item,
            value=data["checks"][item]
        )

    # --------------------
    # メモ
    # --------------------
    st.markdown("### 📝 メモ")
    data["memo"] = st.text_area(
        "気づいたこと",
        value=data["memo"]
    )

    # --------------------
    # 保存
    # --------------------
    if st.button("💾 保存", use_container_width=True):
        save_to_csv(today, data)
        st.success("保存しました")

    # --------------------
    # リセット
    # --------------------
    if st.button("🔄 今日のチェックをリセット", use_container_width=True):
        st.session_state.checklist[today] = {
            "checks": {item: False for item in ITEMS},
            "memo": ""
        }
        delete_today_from_csv(today)
        st.success("リセットしました")

    # --------------------
    # サマリー
    # --------------------
    st.markdown("---")
    st.markdown("### 📅 日別サマリー")

    for date, d in sorted(st.session_state.checklist.items(), reverse=True):
        done = sum(d["checks"].values())
        total = len(d["checks"])
        memo = "📝あり" if d["memo"] else "メモなし"
        st.markdown(f"- **{date}**：{done}/{total} ｜ {memo}")


# ====================
# CSV操作
# ====================
def save_to_csv(date, data):
    os.makedirs("data", exist_ok=True)

    rows = []
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if r["date"] != date]

    row = {"date": date, "memo": data["memo"]}
    for k, v in data["checks"].items():
        row[k] = v

    rows.append(row)

    with open(CHECKLIST_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerows(rows)


def delete_today_from_csv(date):
    if not os.path.exists(CHECKLIST_FILE):
        return

    with open(CHECKLIST_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r["date"] != date]

    if rows:
        with open(CHECKLIST_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.w
