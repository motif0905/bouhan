import streamlit as st
import pandas as pd
import json

def render():
    st.markdown("## 📊 犯罪統計グラフ")

    # CSV読み込み
    df = pd.read_csv("data/processed/crime_summary.csv")


    # ===== デバッグ用（最初は必ず表示）=====
    st.write("📄 CSVの列名:", list(df.columns))

    # ===== 列名をここで合わせる =====
    # 実際のCSVに存在する名前に修正すること
    label_col = df.columns[0]   # 1列目（罪種など）
    value_col = df.columns[1]   # 2列目（件数など）

    labels = df["罪種"].tolist()
    values = df["認知件数_2025"].tolist()

    # ===== Chart.js 用データ =====
    chart_data = {
        "labels": labels,
        "datasets": [
            {
                "label": value_col,
                "data": values
            }
        ]
    }

    chart_json = json.dumps(chart_data, ensure_ascii=False)

    # ===== Chart.js 描画 =====
    st.components.v1.html(
        f"""
        <canvas id="crimeChart"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        const ctx = document.getElementById('crimeChart');
        new Chart(ctx, {{
            type: 'bar',
            data: {chart_json},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        </script>
        """,
        height=500
    )
