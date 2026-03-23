import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(layout="wide")

st.title(" Healthcare Analytics Dashboard")

# ------------------ LOAD DATA ------------------
df = pd.read_excel("medical_dataset.xlsx")

# Add Date column (for filtering)
df["Date"] = pd.date_range(start="2023-01-01", periods=len(df))

# ------------------ SIDEBAR ------------------
st.sidebar.header("Filters")

gender = st.sidebar.multiselect("Select Gender", df["Gender"].unique())
disease = st.sidebar.multiselect("Select Disease", df["Disease"].unique())
date_range = st.sidebar.date_input("Select Date Range", [])

filtered_df = df.copy()

if gender:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender)]

if disease:
    filtered_df = filtered_df[filtered_df["Disease"].isin(disease)]

# Date filter
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Date"] <= pd.to_datetime(date_range[1]))
    ]

# ------------------ KPI CARDS ------------------
total_patients = len(filtered_df)
avg_age = filtered_df["Age"].mean()
avg_bp = filtered_df["BloodPressure"].mean()
avg_chol = filtered_df["Cholesterol"].mean()
most_common_disease = filtered_df["Disease"].mode()[0] if not filtered_df.empty else "N/A"

st.markdown("##  Dashboard Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(" Total Patients", total_patients)
col2.metric(" Avg Age", round(avg_age, 1) if total_patients else 0)
col3.metric(" Avg BP", round(avg_bp, 1) if total_patients else 0)
col4.metric(" Avg Cholesterol", round(avg_chol, 1) if total_patients else 0)
col5.metric(" Top Disease", most_common_disease)

st.markdown("---")

# ------------------ INSIGHTS ------------------
st.subheader(" Key Insights")

if total_patients > 0:
    st.write(f"""
    - Most common disease is **{most_common_disease}**
    - Average patient age is **{round(avg_age,1)}**
    - Average blood pressure is **{round(avg_bp,1)}**
    - Total patients analyzed: **{total_patients}**
    """)
else:
    st.warning("No data available for selected filters")

# ------------------ CHARTS ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Disease Distribution")
    disease_count = filtered_df["Disease"].value_counts().reset_index()
    disease_count.columns = ["Disease", "Count"]

    fig = px.bar(disease_count, x="Disease", y="Count", color="Disease", hover_data=["Count"])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(" Gender Distribution")
    gender_count = filtered_df["Gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "Count"]

    fig = px.pie(gender_count, names="Gender", values="Count", hover_data=["Count"])
    st.plotly_chart(fig, use_container_width=True)

# ------------------ MORE CHARTS ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Age Distribution")
    fig = px.histogram(filtered_df, x="Age", nbins=20)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(" Correlation Heatmap")
    corr = filtered_df.corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")
    st.plotly_chart(fig, use_container_width=True)

# ------------------ OUTCOME ANALYSIS ------------------
st.subheader("Patient Outcome Analysis")

if "Outcome" in filtered_df.columns:
    outcome_count = filtered_df["Outcome"].value_counts().reset_index()
    outcome_count.columns = ["Outcome", "Count"]

    fig = px.bar(outcome_count, x="Outcome", y="Count", color="Outcome")
    st.plotly_chart(fig, use_container_width=True)

# ------------------ TOP DISEASES ------------------
st.subheader(" Top 5 Diseases")

top_diseases = filtered_df["Disease"].value_counts().head(5).reset_index()
top_diseases.columns = ["Disease", "Count"]

fig = px.bar(top_diseases, x="Count", y="Disease", orientation="h", color="Disease")
st.plotly_chart(fig, use_container_width=True)

# ------------------ TABLE ------------------
st.subheader(" Patient Data Table")

st.dataframe(filtered_df, use_container_width=True)

# ------------------ DOWNLOAD BUTTON ------------------
st.download_button(
    label=" Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_medical_data.csv",
    mime="text/csv"
)