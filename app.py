import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page setup ---
st.set_page_config(page_title="K-Pop Insights App", layout="wide")

# --- Zodiac sign calculator ---
def get_zodiac_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19): return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20): return "Pisces"
    else: return "Unknown"

# --- Sidebar: File upload ---
st.sidebar.title("📂 Upload Your K-Pop Data")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # --- Preprocessing ---
    if "Date of Birth" in df.columns:
        df["Date of Birth"] = pd.to_datetime(df["Date of Birth"], errors="coerce")
        df["Zodiac Sign"] = df["Date of Birth"].apply(lambda d: get_zodiac_sign(d.month, d.day) if pd.notnull(d) else "Unknown")
        df["Age"] = pd.to_datetime("today").year - df["Date of Birth"].dt.year

    # --- Sidebar: Navigation ---
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to", [
        "Overview",
        "Groups",
        "Gender Distribution",
        "Visualizations",
        "Zodiac Signs"
    ])

    # --- Sidebar: Filters ---
    st.sidebar.header("🎛️ Filter Options")
    selected_group = st.sidebar.selectbox("🎤 Select Group", ["All"] + sorted(df["Group"].dropna().unique()))
    selected_gender = st.sidebar.multiselect("👤 Select Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    selected_country = st.sidebar.multiselect("🌍 Select Country", df["Country"].dropna().unique())
    search_query = st.sidebar.text_input("🔎 Search Singer by Name", "")

    # --- Filter function ---
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

    # --- Page: Overview ---
    if page == "Overview":
        st.header("📊 K-Pop Dataset Overview")
        st.dataframe(df_filtered)

    # --- Page: Groups ---
    elif page == "Groups":
        st.header("🎶 K-Pop Groups & Members")
        group_counts = df_filtered["Group"].value_counts().reset_index()
        group_counts.columns = ["Group", "Count"]
        fig_group = px.bar(group_counts, x="Group", y="Count", title="Group Sizes", color="Group")
        st.plotly_chart(fig_group)

    # --- Page: Gender Distribution ---
    elif page == "Gender Distribution":
        st.header("👤 Gender Ratio in K-Pop")
        gender_counts = df_filtered["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig_gender = px.pie(gender_counts, names="Gender", values="Count", title="Gender Distribution")
        st.plotly_chart(fig_gender)

    # --- Page: Visualizations ---
    elif page == "Visualizations":
        st.header("📈 K-Pop Visual Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("👵 Top 10 Oldest Idols")
            oldest = df_filtered.dropna(subset=["Age"]).sort_values(by="Age", ascending=False).head(10)
            fig_oldest = px.bar(oldest, x="Stage Name", y="Age", color="Gender", title="Top 10 Oldest Idols")
            st.plotly_chart(fig_oldest)

        with col2:
            st.subheader("👶 Top 10 Youngest Idols")
            youngest = df_filtered.dropna(subset=["Age"]).sort_values(by="Age").head(10)
            fig_youngest = px.bar(youngest, x="Stage Name", y="Age", color="Gender", title="Top 10 Youngest Idols")
            st.plotly_chart(fig_youngest)

        st.subheader("🌍 Idol Count by Country")
        if "Country" in df_filtered.columns:
            country_counts = df_filtered["Country"].value_counts().reset_index()
            country_counts.columns = ["Country", "Count"]
            fig_country = px.bar(
                country_counts,
                x="Country",
                y="Count",
                title="K-Pop Idols by Country",
                color_discrete_sequence=["#20B2AA"]
            )
            st.plotly_chart(fig_country)
        else:
            st.warning("⚠️ 'Country' column not found.")

    # --- Page: Zodiac Signs ---
    elif page == "Zodiac Signs":
        st.header("🔮 Most Common Zodiac Signs in K-Pop")
        if "Zodiac Sign" not in df_filtered.columns:
            st.warning("⚠️ Zodiac Sign column missing.")
        else:
            zodiac_counts = df_filtered["Zodiac Sign"].value_counts().reset_index()
            zodiac_counts.columns = ["Zodiac Sign", "Count"]
            fig_zodiac = px.bar(
                zodiac_counts,
                x="Zodiac Sign",
                y="Count",
                title="Most Common Zodiac Signs",
                color_discrete_sequence=["#6A5ACD"]  # Flat indigo color
            )
            st.plotly_chart(fig_zodiac)

else:
    st.warning("📌 Please upload an Excel file to get started.")
