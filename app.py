import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
df = pd.read_csv("cleaned_periodic_table_2.csv", encoding='ISO-8859-1')

# Phase 필터
phase_list = ["전체"] + sorted(df["phase"].dropna().unique().tolist())
selected_phase = st.selectbox("상태(Phase) 선택", phase_list)

filtered_df = df if selected_phase == "전체" else df[df["phase"] == selected_phase]

# 숫자형 열 선택
numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()
x_axis = st.selectbox("X축 선택", numeric_cols, index=0)
y_axis = st.selectbox("Y축 선택", numeric_cols, index=1)

# 시각화 유형 선택
chart_type = st.radio("시각화 유형을 선택하세요", ("산점도", "막대그래프", "히트맵"))

st.subheader("📊 선택한 시각화")

# 시각화
if chart_type == "산점도":
    fig = px.scatter(
        filtered_df, x=x_axis, y=y_axis,
        hover_name="name", title=f"{x_axis} vs {y_axis}"
    )
    st.plotly_chart(fig)

elif chart_type == "막대그래프":
    bar_df = filtered_df.sort_values(by=y_axis, ascending=False).head(20)
    fig = px.bar(bar_df, x="name", y=y_axis, title=f"{y_axis} 상위 20개 원소")
    st.plotly_chart(fig)

elif chart_type == "히트맵":
    corr = filtered_df[numeric_cols].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
