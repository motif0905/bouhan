import streamlit as st

st.set_page_config(
    page_title="日常防犯ナビ",
    layout="centered"
)

page = st.sidebar.selectbox(
    "メニュー",
    ["トップ", "統計データ", "豆知識", "防犯チェックリスト"]
)

if page == "トップ":
    st.title("🏠 日常防犯ナビ")
    st.write("防犯情報を分かりやすく提供するアプリです。")

elif page == "統計データ":
    st.title("📊 統計データ")
    st.write("※ 準備中")

elif page == "豆知識":
    st.title("📘 防犯豆知識")
    st.write("※ 準備中")


elif page == "防犯チェックリスト":
    st.title("✔ 防犯チェックリスト")
    st.write("※ 準備中")
