import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Cancer Biomarker Explorer", layout="wide")
st.title("🧬 Cancer Biomarker Explorer")

# Sidebar upload
uploaded_file = st.sidebar.file_uploader("📤 Upload a Biomarker CSV", type=["csv"])

# Load data
try:
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
    else:
        df = pd.read_csv("biomarkers.csv")
except Exception as e:
    st.error(f"❌ Failed to read CSV: {e}")
    st.stop()

# Validate columns
required_columns = ["Cancer Type", "Biomarker Category", "Testing Method"]
if not all(col in df.columns for col in required_columns):
    st.error("❌ Uploaded CSV is missing one or more required columns.")
    st.stop()

# Clean missing values
df[required_columns] = df[required_columns].fillna("Unknown")

# 🧼 Normalize & explode Cancer Type
df["Cancer Type"] = df["Cancer Type"].str.replace("|", ",", regex=False)
df["Cancer Type"] = df["Cancer Type"].str.title().str.strip().str.split(",")
df = df.explode("Cancer Type")
df["Cancer Type"] = df["Cancer Type"].str.strip()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

selected_cancer_types = st.sidebar.multiselect(
    "Select Cancer Types:",
    options=sorted(df["Cancer Type"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Biomarker Categories:",
    options=sorted(df["Biomarker Category"].unique())
)

selected_methods = st.sidebar.multiselect(
    "Select Testing Methods:",
    options=sorted(df["Testing Method"].unique())
)

# Apply filters
filtered_df = df.copy()

if selected_cancer_types:
    filtered_df = filtered_df[filtered_df["Cancer Type"].isin(selected_cancer_types)]

if selected_categories:
    filtered_df = filtered_df[filtered_df["Biomarker Category"].isin(selected_categories)]

if selected_methods:
    filtered_df = filtered_df[filtered_df["Testing Method"].isin(selected_methods)]

# Summary text
st.markdown(f"**🔎 {len(filtered_df)} biomarkers match your filters**")

# Data preview
st.dataframe(filtered_df)

# Download button
st.download_button(
    label="📥 Download Filtered Biomarkers as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_biomarkers.csv",
    mime="text/csv"
)


import plotly.express as px

# 📊 Interactive Plotly Visualization
st.subheader("📊 Distribution of Selected Cancer Types")
try:
    chart_counts = filtered_df["Cancer Type"].value_counts().loc[selected_cancer_types].reset_index()
    chart_counts.columns = ["Cancer Type", "Count"]

    fig = px.bar(
        chart_counts,
        x="Cancer Type",
        y="Count",
        title="Cancer Type Distribution",
        color="Cancer Type",
        text="Count",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(xaxis_title="Cancer Type", yaxis_title="Count")
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.warning(f"⚠️ Couldn’t generate Plotly chart: {e}")
  
