import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Set up the Streamlit app
st.set_page_config(page_title="K-Pop Insights App", layout="wide")

# 📌 Zodiac Sign Calculation
def get_zodiac_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    else:
        return "Unknown"

# Upload Excel file
st.sidebar.title("📂 Upload Your K-Pop Data")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Generate Zodiac Signs
    if "Date of Birth" in df.columns:
        df["Date of Birth"] = pd.to_datetime(df["Date of Birth"], errors="coerce")
        df["Zodiac Sign"] = df["Date of Birth"].apply(
            lambda d: get_zodiac_sign(d.month, d.day) if pd.notnull(d) else "Unknown"
        )

    # Navigation
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to", [
        "Overview",
        "Groups",
        "Gender Distribution",
        "Visualizations",
        "Zodiac Signs"
    ])

    # Filters
    st.sidebar.header("🎛️ Filter Options")
    selected_group = st.sidebar.selectbox("🎤 Select Group", ["All"] + sorted(df["Group"].dropna().unique()))
    selected_gender = st.sidebar.multiselect("👤 Select Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    selected_country = st.sidebar.multiselect("🌍 Select Country", df["Country"].dropna().unique())
    search_query = st.sidebar.text_input("🔎 Search Singer by Name", "")

    # Filter Function
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

    # PAGE: Overview
    if page == "Overview":
        st.header("📊 K-Pop Dataset Overview")
        st.dataframe(df_filtered)

    # PAGE: Groups
    elif page == "Groups":
        st.header("🎶 K-Pop Groups & Members")
        group_counts = df_filtered["Group"].value_counts().reset_index()
        group_counts.columns = ["Group", "Count"]
        fig_group = px.bar(group_counts, x="Group", y="Count", title="Group Sizes", color="Group")
        st.plotly_chart(fig_group)

    # PAGE: Gender Distribution
    elif page == "Gender Distribution":
        st.header("👤 Gender Ratio in K-Pop")
        gender_counts = df_filtered["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig_gender = px.pie(gender_counts, names="Gender", values="Count", title="Gender Distribution")
        st.plotly_chart(fig_gender)

    # PAGE: Visualizations
    elif page == "Visualizations":
        st.header("📈 K-Pop Visual Stats")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📏 Height Distribution (Histogram)")
            fig_height = px.histogram(
                df_filtered,
                x="Height",
                nbins=30,
                title="Height Distribution of K-Pop Idols",
                color="Gender"
            )
            st.plotly_chart(fig_height)

        with col2:
            st.subheader("⚖ Weight Distribution (Box Plot)")
            fig_weight = px.box(
                df_filtered,
                y="Weight",
                color="Gender",
                title="Weight Distribution of K-Pop Idols"
            )
            st.plotly_chart(fig_weight)

        st.subheader("📅 Age Distribution (by Birth Year)")
        if "Date of Birth" in df_filtered.columns:
            df_filtered["Birth Year"] = df_filtered["Date of Birth"].dt.year
            fig_age = px.histogram(
                df_filtered.dropna(subset=["Birth Year"]),
                x="Birth Year",
                title="Age Distribution of K-Pop Idols",
                color="Gender"
            )
            st.plotly_chart(fig_age)
        else:
            st.warning("⚠️ 'Date of Birth' column is missing or invalid.")

    # PAGE: Zodiac Signs
    elif page == "Zodiac Signs":
        st.header("🔮 Most Common Zodiac Signs in K-Pop")
        if "Zodiac Sign" not in df_filtered.columns:
            st.warning("⚠️ Zodiac Sign data not found.")
        else:
            zodiac_counts = df_filtered["Zodiac Sign"].value_counts().reset_index()
            zodiac_counts.columns = ["Zodiac Sign", "Count"]
            fig_zodiac = px.bar(
                zodiac_counts,
                x="Zodiac Sign",
                y="Count",
                title="Most Common Zodiac Signs",
                color="Count",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_zodiac)

else:
    st.warning("📌 Please upload an Excel file to begin.")
