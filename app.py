import streamlit as st
import pandas as pd

# Streamlit File Uploader
st.title("🎤 K-Pop Singers Dashboard")
st.write("Upload your K-Pop data file to get started.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Group Filter
    group_list = df["Group"].dropna().unique()
    selected_group = st.selectbox("Select a K-Pop Group", ["All"] + list(group_list))

    # Filter Data
    filtered_df = df if selected_group == "All" else df[df["Group"] == selected_group]

    # Display the filtered results
    st.write(f"Showing results for: **{selected_group}**")
    st.dataframe(filtered_df)
else:
    st.warning("Please upload an Excel file to continue.")
