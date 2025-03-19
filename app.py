import streamlit as st
import pandas as pd

# App Title
st.title("🎤 K-Pop Singers Dashboard")

# Upload File Widget
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")

    # Search Bar
    search_query = st.sidebar.text_input("🔎 Search for a singer (Stage Name)", "")

    # Group Dropdown
    group_list = ["All"] + list(df["Group"].dropna().unique())
    selected_group = st.sidebar.selectbox("🎤 Select a K-Pop Group", group_list)

    # Show All Checkbox
    show_all = st.sidebar.checkbox("Show All Singers", value=True)

    # Filtering Logic
    filtered_df = df.copy()
    if not show_all:
        if selected_group != "All":
            filtered_df = filtered_df[filtered_df["Group"] == selected_group]
        if search_query:
            filtered_df = filtered_df[filtered_df["Stage Name"].str.contains(search_query, case=False, na=False)]

    # Display Results
    st.write(f"Showing results for: **{selected_group}**")
    st.dataframe(filtered_df)

else:
    st.warning("📌 Please upload an Excel file to continue.")
