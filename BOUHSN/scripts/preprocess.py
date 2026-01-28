import pandas as pd
import os
import numpy as np

SHEETS = {
    "高齢者": "高齢者関連事故（１２月中）",
    "こども": "こども関連事故（１２月中）",
    "自転車": "自転車関連事故（１２月中）",
    "歩行者": "歩行者関連事故（１２月中）",
}

def _find_header_row(raw: pd.DataFrame) -> int:
    # どこかに「市区町村」がある行をヘッダー行として採用
    idx = np.where(raw.eq("市区町村"))[0]
    return int(idx[0])

def _pick_area_series(df: pd.DataFrame) -> pd.Series:
    """
    このxlsxは地域名が '市区町村' ではなく、だいたい Unnamed: 3 に入ってる。
    なので以下の優先順で“地域名”を作る：
      1) Unnamed: 3（門司区/若松区/○○市がいる列）
      2) 市区町村（総合計/市部合計などが入ることもあるが、地域名が入る場合もある）
      3) Unnamed: 1（政令市計などがいる）
    """
    candidates = []
    for col in ["Unnamed: 3", "市区町村", "Unnamed: 1"]:
        if col in df.columns:
            candidates.append(df[col].astype("string"))

    if not candidates:
        raise ValueError("地域名に使えそうな列が見つからない（列構造が想定と違う）")

    area = candidates[0]
    for s in candidates[1:]:
        area = area.fillna(s)
    return area

def _read_sheet_tidy(file_path: str, sheet_name: str, accident_label: str) -> pd.DataFrame:
    raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    header_row = _find_header_row(raw)

    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)

    # 発生件数：最初の数値列を採用（列名ブレ対策）
    count_col = df.select_dtypes(include="number").columns[0]

    area = _pick_area_series(df)

    out = pd.DataFrame({
        "地域名": area,
        "事故カテゴリ": accident_label,
        "発生件数": df[count_col],
    })

    # 不要行を落とす（総合計、注釈、空行など）
    out = out.dropna(subset=["地域名", "発生件数"])
    out["地域名"] = out["地域名"].astype(str).str.strip()

    drop_words = ["総合計", "市部合計", "郡部合計", "高速道路等", "政令市計", "計", "小計", "※", "C"]
    out = out[~out["地域名"].isin(drop_words)]
    out = out[~out["地域名"].str.startswith("※")]

    return out[["地域名", "事故カテゴリ", "発生件数"]]

def city_and_ward_labels(name: str) -> list[str]:
    """
    1つの地域名から「〇〇市」と「〇〇区」を両方カテゴリ化（両方出す）
    例：北九州市門司区 → ["北九州市", "門司区"]
        大牟田市 → ["大牟田市"]
        門司区 → ["門司区"]（もし単独表記なら）
    """
    s = str(name)
    labels = []

    if "市" in s:
        labels.append(s.split("市", 1)[0] + "市")
        after_city = s.split("市", 1)[1]
        if after_city.endswith("区"):
            labels.append(after_city)
    elif s.endswith("区"):
        labels.append(s)

    return list(dict.fromkeys(labels))

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    xlsx_path = os.path.join(base_dir, "data", "raw", "sikutyousonbetusubete12.xlsx")
    out_csv = os.path.join(base_dir, "data", "processed", "tidy_accidents.csv")

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    parts = []
    for cat, sheet in SHEETS.items():
        parts.append(_read_sheet_tidy(xlsx_path, sheet, cat))

    tidy = pd.concat(parts, ignore_index=True)

    # 「〇〇市」「〇〇区」を両方カテゴリとして持たせる（行増やし）
    tidy["地域カテゴリ"] = tidy["地域名"].apply(city_and_ward_labels)
    tidy = tidy.explode("地域カテゴリ").dropna(subset=["地域カテゴリ"])
    tidy = tidy[["地域カテゴリ", "事故カテゴリ", "発生件数"]]

    tidy.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print("Saved:", out_csv)
    print("Unique regions:", tidy["地域カテゴリ"].nunique())

if __name__ == "__main__":
    main()
