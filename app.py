import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("cleaned_periodic_table_2.csv", encoding='ISO-8859-1')

st.title("🔬 주기율표 데이터 시각화")

# Phase 필터
phase_list = ["전체"] + sorted(df["phase"].dropna().unique().tolist())
selected_phase = st.selectbox("상태(Phase) 선택", phase_list)

# 상태 필터링
if selected_phase != "전체":
    filtered_df = df[df["phase"] == selected_phase]
else:
    filtered_df = df.copy()

# 숫자형 열 추출
numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# X축, Y축 선택
x_axis = st.selectbox("X축 데이터 선택", numeric_cols, index=0)
y_axis = st.selectbox("Y축 데이터 선택", numeric_cols, index=1)

# 그래프 유형 선택
chart_type = st.radio("📊 그래프 유형 선택", ["산점도 (scatter)", "선 그래프 (line)", "막대그래프 (bar)"])

# 데이터 준비
chart_df = filtered_df[[x_axis, y_axis, "name"]].dropna()

# 시각화
st.subheader("📈 시각화 결과")
if chart_type == "산점도 (scatter)":
    fig = px.scatter(
        chart_df,
        x=x_axis,
        y=y_axis,
        hover_name="name",
        title=f"{x_axis} vs. {y_axis} ({selected_phase} 상태)"
    )
elif chart_type == "선 그래프 (line)":
    fig = px.line(
        chart_df.sort_values(x_axis),
        x=x_axis,
        y=y_axis,
        hover_name="name",
        title=f"{x_axis} vs. {y_axis} 선 그래프 ({selected_phase} 상태)"
    )
elif chart_type == "막대그래프 (bar)":
    fig = px.bar(
        chart_df.sort_values(x_axis),
        x="name",
        y=y_axis,
        hover_name="name",
        title=f"{y_axis} by 원소 이름 (정렬 기준: {x_axis})"
    )

st.plotly_chart(fig)
