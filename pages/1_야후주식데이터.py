import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🇰🇷 한국 시가총액 Top 10 주가 변동 (최근 1년)")

# KRX 시총 상위 10개 기업 (2024 기준)
top10_krx = {
    "삼성전자": "005930.KS",
    "LG에너지솔루션": "373220.KS",
    "SK하이닉스": "000660.KS",
    "삼성바이오로직스": "207940.KS",
    "삼성SDI": "006400.KS",
    "현대차": "005380.KS",
    "LG화학": "051910.KS",
    "NAVER": "035420.KS",
    "기아": "000270.KS",
    "카카오": "035720.KS"
}

with st.spinner("📥 데이터를 불러오는 중입니다..."):
    data = yf.download(list(top10_krx.values()), period="1y")["Adj Close"]
    data.columns = list(top10_krx.keys())

# ✅ Plotly 시각화
fig = go.Figure()
for company in data.columns:
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[company],
        mode='lines',
        name=company
    ))

fig.update_layout(
    title="시가총액 Top 10 기업의 주가 추이 (최근 1년)",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (KRW)",
    hovermode="x unified",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
