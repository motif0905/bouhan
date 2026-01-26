import streamlit as st

st.set_page_config(
    page_title="日常防犯ナビ",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state.page = "menu"

# 左上ホーム
if st.session_state.page != "menu":
    col1, _ = st.columns([1, 6])
    with col1:
        if st.button("戻る"):
            st.session_state.page = "menu"
    st.markdown("---")

# ページ振り分け
if st.session_state.page == "menu":
    import pages.menu as page
elif st.session_state.page == "today_tip":
    import pages.today_tip as page
elif st.session_state.page == "tips":
    import pages.tips_list as page
elif st.session_state.page == "checklist":
    import pages.checklist as page
elif st.session_state.page == "stats":
    import pages.stats as page

page.render()
