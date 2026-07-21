
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
