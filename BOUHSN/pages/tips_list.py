import streamlit as st
from data.tips_data import TIPS

def render():
    st.markdown("## 防犯豆知識一覧")

    # 検索
    keyword = st.text_input("🔍 キーワード検索")

    # カテゴリ
    categories = ["すべて"] + sorted({t["category"] for t in TIPS})
    category = st.selectbox("🏷 カテゴリ", categories)

    st.markdown("---")

    results = []
    for tip in TIPS:
        if keyword and keyword not in tip["text"]:
            continue
        if category != "すべて" and tip["category"] != category:
            continue
        results.append(tip)

    if not results:
        st.warning("該当する豆知識がありません")
        return

    for tip in results:
        st.markdown(f"- **[{tip['category']}]** {tip['text']}")
