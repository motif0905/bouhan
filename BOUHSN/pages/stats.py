import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ====== 文字ボケ対策：Matplotlib設定 ======
plt.rcParams["figure.dpi"] = 200
plt.rcParams["savefig.dpi"] = 200

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK JP", "Noto Sans JP", "IPAexGothic", "IPAGothic",
    "Yu Gothic", "Meiryo", "Hiragino Sans", "MS Gothic"
]
plt.rcParams["axes.unicode_minus"] = False

@st.cache_data
def load_csv(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def render():
    st.title("先月の事故統計(令和7年12月末")

    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "data", "processed", "tidy_accidents.csv")

    df = load_csv(csv_path)

    # 事故カテゴリ名を統一（念のため）
    df["事故カテゴリ"] = df["事故カテゴリ"].replace({
        "自転車関連事故": "自転車",
        "高齢者関連事故": "高齢者",
        "歩行者関連事故": "歩行者",
        "こども関連事故": "こども",
    })

    # 地域リスト
    regions_all = sorted(df["地域カテゴリ"].dropna().unique().tolist())

    # ====== 検索機能 ======
    keyword = st.text_input("地域を検索（例：門司 / 北九州 / 佐賀）", "")

    if keyword.strip():
        regions = [r for r in regions_all if keyword in r]
        if not regions:
            st.warning("該当する地域が見つかりません。検索語を変えてみて。")
            return
    else:
        regions = regions_all

    region = st.selectbox("地域（〇〇市・〇〇区）を選択", regions)

    # 集計
    order = ["自転車", "高齢者", "歩行者", "こども"]
    summary = (
        df[df["地域カテゴリ"] == region]
        .groupby("事故カテゴリ")["発生件数"]
        .sum()
        .reindex(order, fill_value=0)
    )

    if summary.sum() == 0:
        st.warning("この地域の事故データはありません。")
        return

    # 円グラフ
    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=200)
    ax.set_title(f"{region} の事故内訳", fontsize=14)

    ax.pie(
        summary.values,
        labels=summary.index,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 12},
    )
    ax.axis("equal")

    st.pyplot(fig, use_container_width=True)

    st.caption("件数（参考）")
    st.dataframe(summary.rename("発生件数").reset_index())
