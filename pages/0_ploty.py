import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
mf_file = "202504_202504_연령별인구현황_월간_남여구분.csv"
total_file = "202504_202504_연령별인구현황_월간_남여합계.csv"

# CSV 파일 로드
df_mf = pd.read_csv(mf_file, encoding='cp949')
df_total = pd.read_csv(total_file, encoding='cp949')

# 전국 데이터 필터링
df_mf_total = df_mf[df_mf['행정구역'].str.contains('전국')]
df_total_total = df_total[df_total['행정구역'].str.contains('전국')]

# 연령별 컬럼 추출
male_cols = [col for col in df_mf.columns if '2025년04월_남_' in col and '세' in col]
female_cols = [col for col in df_mf.columns if '2025년04월_여_' in col and '세' in col]
total_cols = [col for col in df_total.columns if '2025년04월_계_' in col and '세' in col]

ages = [col.split('_')[-1] for col in total_cols]
male_pop = df_mf_total[male_cols].iloc[0].str.replace(',', '').astype(int).values
female_pop = df_mf_total[female_cols].iloc[0].str.replace(',', '').astype(int).values
total_pop = df_total_total[total_cols].iloc[0].str.replace(',', '').astype(int).values

# Plotly 그래프 생성
fig = go.Figure()
fig.add_trace(go.Scatter(x=ages, y=male_pop, mode='lines+markers', name='남성'))
fig.add_trace(go.Scatter(x=ages, y=female_pop, mode='lines+markers', name='여성'))
fig.add_trace(go.Scatter(x=ages, y=total_pop, mode='lines+markers', name='전체'))

fig.update_layout(
    title='2025년 4월 연령별 인구 현황 (전국)',
    xaxis_title='연령',
    yaxis_title='인구 수',
    hovermode='x unified',
    width=900,
    height=600
)

# Streamlit 앱 출력
st.title("2025년 4월 연령별 인구 현황 (전국)")
st.plotly_chart(fig)
