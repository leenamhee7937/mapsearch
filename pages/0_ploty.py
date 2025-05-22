import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
mf_file = "202504_202504_연령별인구현황_월간_남여구분.csv"
total_file = "202504_202504_연령별인구현황_월간_남여합계.csv"

# 데이터 로드
df_mf = pd.read_csv(mf_file, encoding='cp949')
df_total = pd.read_csv(total_file, encoding='cp949')

# 시도 리스트
region_list = df_total['행정구역'].str.extract(r'([\w\s]+)\s+\(')[0].dropna().unique()

# 선택 메뉴
selected_region = st.selectbox("📍 지역을 선택하세요", region_list)

# 해당 지역 데이터 필터링
df_mf_region = df_mf[df_mf['행정구역'].str.contains(selected_region)]
df_total_region = df_total[df_total['행정구역'].str.contains(selected_region)]

# 컬럼 분류
male_cols = [col for col in df_mf.columns if '2025년04월_남_' in col and '세' in col]
female_cols = [col for col in df_mf.columns if '2025년04월_여_' in col and '세' in col]
total_cols = [col for col in df_total.columns if '2025년04월_계_' in col and '세' in col]
ages = [col.split('_')[-1] for col in total_cols]

# 데이터 정리 함수
def clean_data(series):
    return (
        series
        .str.replace(',', '', regex=False)
        .astype(float)
        .fillna(0)
        .astype(int)
        .values
    )

# 값 추출
male_pop = clean_data(df_mf_region[male_cols].iloc[0])
female_pop = clean_data(df_mf_region[female_cols].iloc[0])
total_pop = clean_data(df_total_region[total_cols].iloc[0])
male_neg = [-x for x in male_pop]

# ✅ 그래프 1: 전체 인구 막대그래프
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(
    x=ages,
    y=total_pop,
    name='전체',
    marker=dict(color='indianred', opacity=0.8),
    hovertemplate='<b>%{x}</b>세<br>인구 수: %{y:,}명<extra></extra>',
))

bar_fig.update_layout(
    title=f'{selected_region} - 연령별 인구 합계 (2025년 4월)',
    xaxis_title='연령',
    yaxis_title='인구 수',
    bargap=0.2,
    hovermode='closest',
    height=500
)

# ✅ 그래프 2: 피라미드 그래프 (남녀 좌우)
pyramid_fig = go.Figure()

pyramid_fig.add_trace(go.Bar(
    y=ages,
    x=male_neg,
    name='남성',
    orientation='h',
    marker=dict(color='rgba(0, 102, 204, 0.8)'),
    hovertemplate='<b>%{y}</b>세<br>남성: %{x:,}명<extra></extra>',
))

pyramid_fig.add_trace(go.Bar(
    y=ages,
    x=female_pop,
    name='여성',
    orientation='h',
    marker=dict(color='rgba(255, 105, 180, 0.8)'),
    hovertemplate='<b>%{y}</b>세<br>여성: %{x:,}명<extra></extra>',
))

pyramid_fig.update_layout(
    title=f'연령별 남녀 인구 피라미드 ({selected_region})',
    xaxis_title='인구수',
    yaxis_title='연령',
    barmode='relative',
    bargap=0.1,
    height=700,
    hovermode='closest',
)

# 📌 Streamlit 출력
st.title("👨‍👩‍👧‍👦 2025년 4월 시도별 연령별 인구 통계")
st.plotly_chart(bar_fig, use_container_width=True)
st.plotly_chart(pyramid_fig, use_container_width=True)
