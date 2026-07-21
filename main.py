
# -------------------------------------------------
# 지역별 범죄 발생건수 - 데이터의 '퍼짐' 보기
# -------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="지역별 범죄 발생건수", page_icon="🚨")

# 데이터 불러오기 (cp949 인코딩)
CSV_PATH = os.path.join(os.path.dirname(__file__), "crime_by_region.csv")
df = pd.read_csv(CSV_PATH, encoding="utf-8")

st.title("🚨 지역별 범죄 발생건수")

# 지역(열)마다 모든 범죄 건수를 더해 '총발생건수' 표 만들기
region_cols = df.columns[2:]
total = df[region_cols].sum().reset_index()
total.columns = ["지역", "총발생건수"]

st.write(total["총발생건수"].describe())

fig1 = px.histogram(total, x="총발생건수", title="총발생건수 히스토그램")
st.plotly_chart(fig1)

fig2 = px.box(total, y="총발생건수", title="총발생건수 상자그림")
st.plotly_chart(fig2)


st.header("지역별 대시보드")

# 시도 -> 지역 고르기
sido = st.selectbox("시도 선택", sorted({c.split(" ")[0] for c in region_cols}))
region = st.selectbox("지역 선택", sorted([c for c in region_cols if c.split(" ")[0] == sido]))

# 지표 카드 3개
top = df.loc[df[region].idxmax()]
c1, c2, c3 = st.columns(3)
c1.metric("총 발생건수", f"{int(df[region].sum()):,}건")
c2.metric("가장 많은 범죄", top["범죄중분류"])
c3.metric("강력범죄", f"{int(df[df['범죄대분류'] == '강력범죄'][region].sum()):,}건")

# 범죄 종류별 막대그래프
by_major = df.groupby("범죄대분류")[region].sum().sort_values(ascending=False).reset_index()
fig3 = px.bar(by_major, x="범죄대분류", y=region, title=f"{region} 범죄 종류별 발생건수")
st.plotly_chart(fig3)
