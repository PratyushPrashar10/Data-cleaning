import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="CleanSight", layout="wide")
st.title("🧼 CleanSight: Data Cleaning & Profiling Dashboard")

# Upload section
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Preview of Uploaded Data")
    num_rows = st.slider(
    "Select number of rows to display", 
    min_value=5, 
    max_value=min(len(df), 1000),  # cap it to avoid browser slowdown
    value=10
)
    st.dataframe(df.head(num_rows))


    # Show basic info
    st.markdown("### 📊 Dataset Summary")
    st.write(f"**Rows:** {df.shape[0]}  |  **Columns:** {df.shape[1]}")
    
    # Missing values
    st.markdown("### 🩹 Missing Values")
    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Values"]
    missing["% Missing"] = 100 * missing["Missing Values"] / df.shape[0]
    st.dataframe(missing[missing["Missing Values"] > 0])

    # Duplicates
    st.markdown("### 📁 Duplicates")
    st.write(f"**Duplicate rows:** {df.duplicated().sum()}")

    # Data types
    st.markdown("### 🧬 Column Types")
    dtypes_df = pd.DataFrame(df.dtypes, columns=["Data Type"])
    st.dataframe(dtypes_df.transpose())

    # Option to drop duplicates
    if st.button("✨ Clean Duplicates"):
        df = df.drop_duplicates()
        st.success("Duplicates removed!")

    # Download cleaned data
    st.markdown("### ⬇️ Download Cleaned Dataset")
    st.download_button("Download CSV", df.to_csv(index=False), "cleaned_data.csv", "text/csv")