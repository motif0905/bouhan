import streamlit as st
from data.tips_data import TIPS
from utils.helpers import get_today_tip, truncate_text

def render():
    st.markdown("## 日常防犯ナビ")

    st.markdown("### 今日の防犯豆知識 ")
    tip = get_today_tip(TIPS)
    st.info(truncate_text(tip["text"]))

    if st.button("もっと見る ▶", use_container_width=True):
        st.session_state.selected_tip = tip
        st.session_state.page = "today_tip"

    st.markdown("### メニュー")

    if st.button("📘 豆知識一覧", use_container_width=True):
        st.session_state.page = "tips"

    if st.button("📊 統計データを見る", use_container_width=True):
        st.session_state.page = "stats"

    if st.button("✅ 防犯チェックリスト", use_container_width=True):
        st.session_state.page = "checklist"
