import streamlit as st

def render():
    tip = st.session_state.selected_tip
    st.markdown("## 今日の防犯豆知識（詳細）")
    st.markdown(f"**カテゴリ**：{tip['category']}")
    st.markdown(f"**内容**：{tip['text']}")
