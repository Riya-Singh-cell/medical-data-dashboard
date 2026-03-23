import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Healthcare Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
h1 {
    text-align: center;
    color: #4CAF50;
}
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1f2937, #111827);
    border-radius: 12px;
    padding: 15px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1> Healthcare Analytics Dashboard</h1>", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
with st.spinner("Loading data..."):
    df = pd.read_excel("medical_dataset.xlsx")

# Add Date column
df["Date"] = pd.date_range(start="2023-01-01", periods=len(df))

# ------------------ SIDEBAR ------------------
st.sidebar.header(" Filters")

gender = st.sidebar.multiselect("Select Gender", df["Gender"].unique())
disease = st.sidebar.multiselect("Select Disease", df["Disease"].unique())
date_range = st.sidebar.date_input("Select Date Range", [])

filtered_df = df.copy()

if gender:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender)]

if disease:
    filtered_df = filtered_df[filtered_df["Disease"].isin(disease)]

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Date"] <= pd.to_datetime(date_range[1]))
    ]

# ------------------ KPI SECTION ------------------
st.markdown("##  Dashboard Overview")

total_patients = len(filtered_df)
avg_age = filtered_df["Age"].mean()
avg_bp = filtered_df["BloodPressure"].mean()
avg_chol = filtered_df["Cholesterol"].mean()
most_common_disease = filtered_df["Disease"].mode()[0] if not filtered_df.empty else "N/A"

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(" Patients", total_patients)
col2.metric(" Avg Age", round(avg_age, 1) if total_patients else 0)
col3.metric(" Avg BP", round(avg_bp, 1) if total_patients else 0)
col4.metric(" Cholesterol", round(avg_chol, 1) if total_patients else 0)
col5.metric(" Top Disease", most_common_disease)

st.markdown("---")

# ------------------ AI INSIGHTS ------------------
st.subheader(" AI Insights")

if total_patients > 0:
    insight = f"""
     **{most_common_disease}** is the most frequent disease.

     Average age (**{round(avg_age,1)}**) shows dominant age group.

     Blood pressure (**{round(avg_bp,1)}**) indicates possible health risks.

     Total patients analyzed: **{total_patients}**
    """
    st.success(insight)
else:
    st.warning("No data available for selected filters")

# ------------------ CHARTS ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Disease Distribution")

    disease_count = filtered_df["Disease"].value_counts().reset_index()
    disease_count.columns = ["Disease", "Count"]

    fig = px.bar(
        disease_count,
        x="Disease",
        y="Count",
        color="Disease",
        hover_data=["Count"]
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(" Gender Distribution")

    gender_count = filtered_df["Gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "Count"]

    fig = px.pie(
        gender_count,
        names="Gender",
        values="Count",
        hover_data=["Count"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------ SECOND ROW ------------------
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
st.subheader(" Patient Outcome Analysis")

if "Outcome" in filtered_df.columns:
    outcome_count = filtered_df["Outcome"].value_counts().reset_index()
    outcome_count.columns = ["Outcome", "Count"]

    fig = px.bar(
        outcome_count,
        x="Outcome",
        y="Count",
        color="Outcome"
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------ TOP DISEASES ------------------
st.subheader(" Top 5 Diseases")

top_diseases = filtered_df["Disease"].value_counts().head(5).reset_index()
top_diseases.columns = ["Disease", "Count"]

fig = px.bar(
    top_diseases,
    x="Count",
    y="Disease",
    orientation="h",
    color="Disease"
)
st.plotly_chart(fig, use_container_width=True)

# ------------------ TABLE ------------------
st.subheader(" Patient Data Table")
st.dataframe(filtered_df, use_container_width=True)

# ------------------ DOWNLOAD ------------------
st.download_button(
    " Download Data",
    data=filtered_df.to_csv(index=False),
    file_name="medical_data.csv",
    mime="text/csv"
)