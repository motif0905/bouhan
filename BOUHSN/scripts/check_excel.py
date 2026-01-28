import pandas as pd

df = pd.read_excel(
    "data/raw/sikutyousonbetusubete12.xlsx",
    engine="openpyxl"
)

print(df.head())
print(df.columns)
