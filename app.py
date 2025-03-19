import streamlit as st
import pandas as pd
import plotly.express as px

# Load Dataset
st.set_page_config(page_title="K-Pop Insights App", layout="wide")

# Upload File
st.sidebar.title("📂 Upload Your K-Pop Data")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Sidebar Navigation
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Groups", "Gender Distribution", "Visualizations"])

    # Sidebar Filters
    st.sidebar.header("🎛️ Filter Options")
    selected_group = st.sidebar.selectbox("🎤 Select Group", ["All"] + sorted(df["Group"].dropna().unique()))
    selected_gender = st.sidebar.multiselect("👤 Select Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    selected_country = st.sidebar.multiselect("🌍 Select Country", df["Country"].dropna().unique())
    search_query = st.sidebar.text_input("🔎 Search Singer by Name", "")

    # Apply Filters
    def filter_data(data):
        filtered_data = data.copy()
        if selected_group != "All":
            filtered_data = filtered_data[filtered_data["Group"] == selected_group]
        if selected_gender:
            filtered_data = filtered_data[filtered_data["Gender"].isin(selected_gender)]
        if selected_country:
            filtered_data = filtered_data[filtered_data["Country"].isin(selected_country)]
        if search_query:
            filtered_data = filtered_data[filtered_data["Stage Name"].str.contains(search_query, case=False, na=False)]
        return filtered_data

    df_filtered = filter_data(df)

    # Navigation Handling
    if page == "Overview":
        st.header("📊 K-Pop Dataset Overview")
        st.dataframe(df_filtered)

    elif page == "Groups":
        st.header("🎶 K-Pop Groups & Members")
        group_counts = df_filtered["Group"].value_counts().reset_index()
        group_counts.columns = ["Group", "Count"]
        fig_group = px.bar(group_counts, x="Group", y="Count", title="K-Pop Groups with Most Members", color="Group")
        st.plotly_chart(fig_group)

    elif page == "Gender Distribution":
        st.header("👤 K-Pop Gender Distribution")
        gender_counts = df_filtered["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig_gender = px.pie(gender_counts, names="Gender", values="Count", title="Gender Ratio in K-Pop")
        st.plotly_chart(fig_gender)

    elif page == "Visualizations":
        st.header("📈 K-Pop Stats: Height & Weight")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📏 Height Distribution")
            fig_height = px.histogram(df_filtered, x="Height", title="Height Distribution of K-Pop Idols", color="Gender")
            st.plotly_chart(fig_height)

        with col2:
            st.subheader("⚖ Weight Distribution")
            fig_weight = px.histogram(df_filtered, x="Weight", title="Weight Distribution of K-Pop Idols", color="Gender")
            st.plotly_chart(fig_weight)

        st.subheader("📅 Age Distribution")
        fig_age = px.histogram(df_filtered, x=pd.to_datetime(df_filtered["Date of Birth"]).dt.year, title="Age Distribution of K-Pop Idols", color="Gender")
        st.plotly_chart(fig_age)

else:
    st.warning("📌 Please upload an Excel file to continue.")
