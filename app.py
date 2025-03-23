import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit Page Configuration
st.set_page_config(page_title="K-Pop Insights App", layout="wide")

# Sidebar - File Upload
st.sidebar.title("📂 Upload Your K-Pop Data")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    # Load Data
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Sidebar Navigation
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to", [
        "Overview",
        "Groups",
        "Gender Distribution",
        "Visualizations",
        "Zodiac Signs"
    ])

    # Sidebar Filters
    st.sidebar.header("🎛️ Filter Options")
    selected_group = st.sidebar.selectbox("🎤 Select Group", ["All"] + sorted(df["Group"].dropna().unique()))
    selected_gender = st.sidebar.multiselect("👤 Select Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    selected_country = st.sidebar.multiselect("🌍 Select Country", df["Country"].dropna().unique())
    search_query = st.sidebar.text_input("🔎 Search Singer by Name", "")

    # Data Filtering Function
    def filter_data(data):
        filtered = data.copy()
        if selected_group != "All":
            filtered = filtered[filtered["Group"] == selected_group]
        if selected_gender:
            filtered = filtered[filtered["Gender"].isin(selected_gender)]
        if selected_country:
            filtered = filtered[filtered["Country"].isin(selected_country)]
        if search_query:
            filtered = filtered[filtered["Stage Name"].str.contains(search_query, case=False, na=False)]
        return filtered

    df_filtered = filter_data(df)

    # NAVIGATION: Overview
    if page == "Overview":
        st.header("📊 K-Pop Dataset Overview")
        st.dataframe(df_filtered)

    # NAVIGATION: Groups
    elif page == "Groups":
        st.header("🎶 K-Pop Groups & Members")
        group_counts = df_filtered["Group"].value_counts().reset_index()
        group_counts.columns = ["Group", "Count"]
        fig_group = px.bar(group_counts, x="Group", y="Count", title="K-Pop Groups with Most Members", color="Group")
        st.plotly_chart(fig_group)

    # NAVIGATION: Gender Distribution
    elif page == "Gender Distribution":
        st.header("👤 K-Pop Gender Distribution")
        gender_counts = df_filtered["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig_gender = px.pie(gender_counts, names="Gender", values="Count", title="Gender Ratio in K-Pop")
        st.plotly_chart(fig_gender)

    # NAVIGATION: Visualizations
    elif page == "Visualizations":
        st.header("📈 K-Pop Stats: Height, Weight & Age")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📏 Height Distribution")
            fig_height = px.histogram(df_filtered, x="Height", title="Height Distribution", color="Gender")
            st.plotly_chart(fig_height)

        with col2:
            st.subheader("⚖ Weight Distribution")
            fig_weight = px.histogram(df_filtered, x="Weight", title="Weight Distribution", color="Gender")
            st.plotly_chart(fig_weight)

        st.subheader("📅 Age Distribution (by Birth Year)")
        if "Date of Birth" in df_filtered.columns:
            df_filtered["Birth Year"] = pd.to_datetime(df_filtered["Date of Birth"], errors="coerce").dt.year
            fig_age = px.histogram(df_filtered.dropna(subset=["Birth Year"]), x="Birth Year", title="Age Distribution", color="Gender")
            st.plotly_chart(fig_age)
        else:
            st.warning("The dataset doesn't include a 'Date of Birth' column.")

    # NAVIGATION: Zodiac Signs
    elif page == "Zodiac Signs":
        st.header("🔮 Most Common Zodiac Signs in K-Pop")

        if "Zodiac Sign" not in df_filtered.columns:
            st.warning("Zodiac Sign data not found in the dataset.")
        else:
            # Count zodiac sign occurrences
            zodiac_counts = df_filtered["Zodiac Sign"].value_counts().reset_index()
            zodiac_counts.columns = ["Zodiac Sign", "Count"]

            # Create a bar chart based on Zodiac Signs
            fig = px.bar(
                zodiac_counts,
                x="Zodiac Sign",
                y="Count",
                title="Most Common Zodiac Signs in K-Pop",
                color="Count",
                color_continuous_scale="Blues"
            )

            st.plotly_chart(fig)

else:
    st.warning("📌 Please upload an Excel file to get started.")
