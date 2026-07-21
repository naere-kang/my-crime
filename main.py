
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

# 평균선(빨강)과 중앙값선(파랑)을 그어서 둘이 벌어진 걸 눈으로 보이게
fig1.add_vline(x=total["총발생건수"].mean(), line_color="red", line_dash="dash", annotation_text="평균 6,409건")
fig1.add_vline(x=total["총발생건수"].median(), line_color="blue", line_dash="dash", annotation_text="중앙값 3,715건")
st.plotly_chart(fig1)
st.caption("막대가 왼쪽에 몰려 있고 오른쪽 꼬리가 깁니다. 평균(빨강)이 중앙값(파랑)보다 오른쪽에 있죠? 범죄가 많은 대도시 몇 곳이 평균을 끌어올린 것입니다.")

fig2 = px.box(total, y="총발생건수", title="총발생건수 상자그림")
st.plotly_chart(fig2)
st.caption("상자 = 가운데 절반의 지역들이 있는 구간(1,110건~9,489건). 상자 위로 튀어나온 점 = 범죄가 유난히 많은 대도시(이상치). 이 점들이 평균을 끌어올린 범인입니다.")


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
