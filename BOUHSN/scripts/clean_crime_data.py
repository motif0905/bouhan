import pandas as pd

# ==========
# 1. 読み込み
# ==========
df = pd.read_csv(
    "../data/raw/r07_1-11.csv",
    encoding="cp932"
)

# ==========
# 2. 不要な上部行を削除
# （実データは index=4 以降）
# ==========
df = df.iloc[4:].reset_index(drop=True)

# ==========
# 3. 必要な列だけ残す
# ==========
df = df.iloc[:, :5]
df.columns = [
    "罪種",
    "認知件数_2025",
    "認知件数_2024",
    "増減",
    "増減率"
]

# ==========
# 4. 数値を数値型に変換
# ==========
for col in ["認知件数_2025", "認知件数_2024", "増減", "増減率"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========
# 5. NaN行（空行）を削除
# ==========
df = df.dropna(subset=["罪種"])

# ==========
# 6. 保存
# ==========
df.to_csv(
    "../data/processed/crime_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("整形完了：crime_summary.csv を作成しました")
