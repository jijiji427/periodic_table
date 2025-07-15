import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
df = pd.read_csv("cleaned_periodic_table_2.csv", encoding='ISO-8859-1')

st.title("🔬 주기율표 데이터 시각화")

# Phase 필터
phase_list = ["전체"] + sorted(df["phase"].dropna().unique().tolist())
selected_phase = st.selectbox("상태(Phase) 선택", phase_list)

# '전체'가 아니라면 해당 상태로 필터링
if selected_phase != "전체":
    filtered_df = df[df["phase"] == selected_phase]
else:
    filtered_df = df.copy()
# 숫자형 열만 추출 (문자형/범주형 제외)
numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# X축, Y축 선택
x_axis = st.selectbox("X축 데이터 선택", numeric_cols, index=0)
y_axis = st.selectbox("Y축 데이터 선택", numeric_cols, index=1)

# 산점도 시각화
st.subheader("📈 산점도")
scatter_df = filtered_df[[x_axis, y_axis, "name"]].dropna()

import plotly.express as px

fig = px.scatter(
    scatter_df,
    x=x_axis,
    y=y_axis,
    hover_name="name",
    title=f"{x_axis} vs. {y_axis} ({selected_phase} 상태 필터)" if selected_phase != "전체" else f"{x_axis} vs. {y_axis} (전체)"
)
st.plotly_chart(fig)
