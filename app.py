import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎬 Netflix Data Analysis Dashboard")

st.markdown(
    """
    **Interactive dashboard for exploring Netflix Movies and TV Shows**

    Analyze Netflix content distribution, countries, release trends,
    ratings, and genres using interactive visualizations.
    """
)


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(
            "netflix_titles.csv",
            encoding="latin1"
        )
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

    return df


df = load_data()


# Stop application if dataset is empty
if df.empty:
    st.error("Dataset could not be loaded.")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the Netflix dataset."
)


# Content Type Filter

content_types = (
    ["All"]
    + sorted(
        df["type"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_type = st.sidebar.selectbox(
    "Content Type",
    content_types
)


# Rating Filter

ratings = (
    ["All"]
    + sorted(
        df["rating"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_rating = st.sidebar.selectbox(
    "Rating",
    ratings
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()


if selected_type != "All":

    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]


if selected_rating != "All":

    filtered_df = filtered_df[
        filtered_df["rating"] == selected_rating
    ]


# Filtered titles in sidebar

st.sidebar.metric(
    "Filtered Titles",
    len(filtered_df)
)


# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

st.subheader("📊 Dataset Overview")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Titles",
        len(filtered_df)
    )


with col2:

    st.metric(
        "Movies",
        (
            filtered_df["type"] == "Movie"
        ).sum()
    )


with col3:

    st.metric(
        "TV Shows",
        (
            filtered_df["type"] == "TV Show"
        ).sum()
    )


# --------------------------------------------------
# DATASET PREVIEW
# --------------------------------------------------

st.subheader("📋 Netflix Dataset")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)


# --------------------------------------------------
# DOWNLOAD FILTERED DATASET
# --------------------------------------------------

st.subheader("⬇️ Download Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_netflix_data.csv",
    mime="text/csv",
    key="download_filtered_data"
)


# --------------------------------------------------
# MOVIES VS TV SHOWS
# --------------------------------------------------

st.subheader("📊 Movies vs TV Shows")


content_count = (
    filtered_df["type"]
    .value_counts()
    .reset_index()
)

content_count.columns = [
    "Type",
    "Count"
]


fig = px.bar(
    content_count,
    x="Type",
    y="Count",
    title="Movies vs TV Shows Distribution",
    text="Count"
)


fig.update_traces(
    textposition="outside"
)


st.plotly_chart(
    fig,
    use_container_width=True,
    key="movies_tv_chart"
)


# --------------------------------------------------
# TOP 10 COUNTRIES
# --------------------------------------------------

st.subheader(
    "🌍 Top 10 Countries Producing Netflix Content"
)


country_data = (
    filtered_df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
    .reset_index()
)

country_data.columns = [
    "Country",
    "Count"
]


fig_country = px.bar(
    country_data,
    x="Count",
    y="Country",
    orientation="h",
    title="Top 10 Countries Producing Netflix Content",
    text="Count"
)


fig_country.update_traces(
    textposition="outside"
)


st.plotly_chart(
    fig_country,
    use_container_width=True,
    key="top_countries_chart"
)


# --------------------------------------------------
# NETFLIX CONTENT GROWTH
# --------------------------------------------------

st.subheader(
    "📈 Netflix Content Growth Over Years"
)


year_data = (
    filtered_df["release_year"]
    .dropna()
    .value_counts()
    .sort_index()
    .reset_index()
)

year_data.columns = [
    "Year",
    "Count"
]


fig_year = px.line(
    year_data,
    x="Year",
    y="Count",
    title="Netflix Content Growth by Release Year",
    markers=True
)


fig_year.update_traces(
    hovertemplate="Year: %{x}<br>Titles: %{y}<extra></extra>"
)


st.plotly_chart(
    fig_year,
    use_container_width=True,
    key="content_growth_chart"
)


# --------------------------------------------------
# RATING ANALYSIS
# --------------------------------------------------

st.subheader(
    "⭐ Netflix Content Ratings"
)


rating_data = (
    filtered_df["rating"]
    .dropna()
    .value_counts()
    .reset_index()
)

rating_data.columns = [
    "Rating",
    "Count"
]


fig_rating = px.bar(
    rating_data,
    x="Rating",
    y="Count",
    title="Netflix Content by Rating",
    text="Count"
)


fig_rating.update_traces(
    textposition="outside"
)


st.plotly_chart(
    fig_rating,
    use_container_width=True,
    key="rating_analysis_chart"
)


# --------------------------------------------------
# TOP 10 GENRES
# --------------------------------------------------

st.subheader(
    "🎭 Top 10 Netflix Genres"
)


genre_data = (
    filtered_df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
    .reset_index()
)

genre_data.columns = [
    "Genre",
    "Count"
]


fig_genre = px.bar(
    genre_data,
    x="Count",
    y="Genre",
    orientation="h",
    title="Top 10 Netflix Genres",
    text="Count"
)


fig_genre.update_traces(
    textposition="outside"
)


st.plotly_chart(
    fig_genre,
    use_container_width=True,
    key="top_genres_chart"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    ### 📌 Project Information

    **Project:** Netflix Data Analysis

    **Technologies:** Python, Pandas, NumPy, Matplotlib, Seaborn,
    Plotly, Streamlit, Jupyter Notebook

    **Author:** Muntha Shirisha
    """
)