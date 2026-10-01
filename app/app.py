import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "netflix_titles_clean.csv"
ASSETS = ROOT / "assets"

st.set_page_config(
    page_title="Netflix Analytics",
    page_icon=str(ASSETS / "branding" / "logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)



# -----------------------------

# Data

# -----------------------------

@st.cache_data(show_spinner=False)

def load_data():

    data = pd.read_csv(DATA)

    data["date_added"] = pd.to_datetime(data["date_added"], errors="coerce")

    for col in ["type", "rating", "country_primary", "listed_in_primary"]:

        data[col] = data[col].fillna("Unknown")

    data["release_year"] = pd.to_numeric(data["release_year"], errors="coerce")

    data["duration_value"] = pd.to_numeric(data["duration_value"], errors="coerce")

    data["year_added"] = pd.to_numeric(data["year_added"], errors="coerce")

    data["month_added"] = data["month_added"].fillna("Unknown")

    return data





df = load_data()



# -----------------------------

# Assets / helpers

# -----------------------------

def img64(path: Path) -> str:

    if not path.exists():

        return ""

    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"

    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()





def asset(folder: str, name: str) -> Path:

    return ASSETS / folder / name





def icon(name: str) -> str:

    return img64(asset("icons", name))





def kpi_icon(name: str) -> str:

    return img64(asset("kpi", name))





def reset_filters():

    for key in ["type_filter", "country_filter", "genre_filter", "rating_filter", "year_filter"]:

        st.session_state.pop(key, None)





NAV = [

    ("Home", "home.png"),

    ("Overview", "overview.png"),

    ("Movies", "movies.png"),

    ("TV Shows", "tvshows.png"),

    ("Countries", "countries.png"),

    ("Genres", "genres.png"),

    ("Ratings", "ratings.png"),

    ("Trends", "trends.png"),

    ("Filters", "filter.png"),

]



# -----------------------------

# Theme

# -----------------------------

st.markdown(

    """

<style>

:root { --red:#F61F35; --red2:#F61F35; --bg:#07090b; --panel:#111417; --panel2:#171a1e; --line:#272d33; --text:#f6f6f7; --muted:#a6adb5; }

.stApp { background:#07090b; color:var(--text); }

[data-testid="stHeader"] { background:transparent; }

.block-container { max-width:1540px; padding:1.05rem 1.15rem 2.5rem; }

section[data-testid="stSidebar"] { background:linear-gradient(180deg,#090b0e 0%,#050607 100%); border-right:1px solid #20252a; }

section[data-testid="stSidebar"] > div { padding:.85rem .75rem; }

.sidebar-logo { padding:7px 10px 20px; border-bottom:1px solid #24292f; margin-bottom:14px; }

.sidebar-logo img { width:100%; max-width:182px; }

.stButton > button { border-radius:10px!important; border:1px solid transparent!important; background:transparent!important; color:#c9ced5!important; text-align:left!important; min-height:40px!important; font-size:14px!important; font-weight:600!important; padding:0 11px!important; }

.stButton > button:hover { background:#181b20!important; border-color:#292f36!important; color:#fff!important; }

.nav-active .stButton > button { background:linear-gradient(90deg,#7f101b,#4f0c13)!important; color:#fff!important; border-color:#99151c!important; }

.filter-card { background:#101317; border:1px solid #242a30; border-radius:14px; padding:13px 13px 9px; margin-top:12px; }

.filter-title { font-size:13px; font-weight:800; color:#fff; margin-bottom:8px; }

.stSelectbox label, .stMultiSelect label, .stSlider label { color:#e8e9eb!important; font-size:12px!important; }

div[data-baseweb="select"] > div { background:#15181c!important; border-color:#363c43!important; color:#fff!important; }

.hero { min-height:300px; border-radius:16px; overflow:hidden; position:relative; background-size:cover; background-position:center; border:1px solid #20252a; box-shadow:0 16px 50px rgba(0,0,0,.34); }

.hero-overlay { min-height:300px; display:flex; align-items:center; padding:34px 42px; background:linear-gradient(90deg,rgba(0,0,0,.98) 0%,rgba(0,0,0,.86) 34%,rgba(0,0,0,.23) 73%,rgba(0,0,0,.04) 100%); }

.hero-copy { max-width:500px; }

.hero-kicker { font-size:12px; letter-spacing:5px; color:#eee; margin-bottom:4px; }

.hero-title { font-size:62px; line-height:.92; font-weight:950; color:#ed1c24; letter-spacing:-2px; margin:0; }

.hero-title span { display:block; color:#fff; font-size:45px; letter-spacing:-1px; margin-top:7px; }

.hero-copy p { color:#d4d4d4; font-size:14px; line-height:1.55; margin:17px 0; max-width:440px; }

.hero-btn { display:inline-block; background:#F61F35; color:#fff; padding:11px 23px; border-radius:24px; font-weight:800; }

.page-head { display:flex; align-items:end; justify-content:space-between; gap:15px; margin:4px 0 17px; }

.page-title { font-size:30px; font-weight:900; margin:0; }

.page-subtitle { color:#9299a2; font-size:13px; margin-top:4px; }

.section-title { font-size:19px; font-weight:850; margin:18px 0 9px; }

.kpi-card { background:linear-gradient(145deg,#14171b,#0d0f12); border:1px solid #262c32; border-radius:13px; padding:13px 14px; min-height:95px; display:flex; align-items:center; gap:11px; box-shadow:0 6px 18px rgba(0,0,0,.16); }

.kpi-icon { width:44px; height:44px; object-fit:contain; filter:drop-shadow(0 0 6px rgba(246,31,53,.22)); }

.kpi-label { color:#c7cbd0; font-size:12px; }

.kpi-value { color:#fff; font-size:25px; font-weight:850; margin-top:3px; }

.kpi-trend { color:#F61F35; font-size:25px; margin-left:auto; }

.metric-box { background:#101316; border:1px solid #23282e; border-radius:12px; padding:13px 15px; }

.metric-label { color:#939ba4; font-size:11px; text-transform:uppercase; letter-spacing:.7px; }

.metric-value { font-size:22px; font-weight:850; margin-top:3px; }

.card { background:#101316; border:1px solid #23282e; border-radius:14px; padding:10px 13px 6px; }

.poster-card { background:#111418; border:1px solid #252a30; border-radius:10px; padding:7px; height:100%; }

.poster-card img { width:100%; height:185px; object-fit:cover; border-radius:7px; }

.poster-title { font-size:12px; font-weight:750; margin-top:7px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

.poster-meta { font-size:11px; color:#aeb4bc; margin-top:3px; }

.rating { color:#ffd84d; }

.small-muted { color:#8f969f; font-size:12px; }

.pill { display:inline-block; padding:4px 9px; border-radius:20px; background:#261013; color:#ff6b72; border:1px solid #4b171c; font-size:11px; font-weight:700; margin-right:5px; }

.stDownloadButton > button { background:#161a1f!important; color:#fff!important; border:1px solid #30363d!important; border-radius:9px!important; }

footer { visibility:hidden; height:0; }


/* =========================================
   YEARLY GROWTH CARDS
========================================= */

.growth-year-card {
    position: relative;
    overflow: hidden;
    cursor: default;
    min-height: 105px;
}

.growth-year-card::before {
    content: "";
    position: absolute;
    width: 90px;
    height: 90px;
    right: -35px;
    bottom: -45px;
    border-radius: 50%;
    background: rgba(246,31,53,.08);
    transition: all .4s ease;
}

.growth-year-card:hover {
    transform: translateY(-6px);
    border-color: rgba(246,31,53,.5);
    box-shadow: 0 12px 30px rgba(246,31,53,.12);
}

.growth-year-card:hover::before {
    width: 140px;
    height: 140px;
    right: -55px;
    bottom: -70px;
    background: rgba(246,31,53,.16);
}

.growth-change {
    margin-top: 7px;
    color: #F61F35;
    font-size: 12px;
    font-weight: 800;
}


/* Copyright */
.copyright {
    margin-top: 45px;
    padding: 18px 0 8px;
    border-top: 1px solid #252a30;
    text-align: center;
    color: #777f88;
    font-size: 12px;
    letter-spacing: .2px;
}
.copyright strong {
    color: #f6f6f7;
}
.copyright a {
    color: #F61F35;
    text-decoration: none;
    font-weight: 700;
    transition: color .25s ease, text-shadow .25s ease;
}
.copyright a:hover {
    color: #ff5968;
    text-shadow: 0 0 10px rgba(246,31,53,.35);
}
.copyright span {
    color: #454b52;
}

</style>

""",

    unsafe_allow_html=True,

)



# -----------------------------

# Sidebar

# -----------------------------

if "page" not in st.session_state:

    st.session_state.page = "Home"



with st.sidebar:

    logo = img64(asset("branding", "netflix_analytics_logo.png"))

    if logo:

        st.markdown(f'<div class="sidebar-logo"><img src="{logo}"></div>', unsafe_allow_html=True)



    for label, icon_name in NAV:

        active = st.session_state.page == label

        c1, c2 = st.columns([0.23, 0.77], vertical_alignment="center")

        with c1:

            data = icon(icon_name)

            if data:

                st.markdown(f'<img src="{data}" style="width:24px;height:24px;object-fit:contain;margin-top:5px;filter:drop-shadow(0 0 5px rgba(246,31,53,.18));">', unsafe_allow_html=True)

        with c2:

            if st.button(label, key=f"nav_{label}", use_container_width=True):

                st.session_state.page = label

                st.rerun()



    st.markdown('<div class="filter-card"><div class="filter-title">Global Filters</div>', unsafe_allow_html=True)

    types = ["All"] + sorted(df["type"].unique().tolist())

    countries = ["All"] + sorted([x for x in df["country_primary"].unique() if x != "Unknown"])

    genres = ["All"] + sorted([x for x in df["listed_in_primary"].unique() if x != "Unknown"])

    ratings = ["All"] + sorted([x for x in df["rating"].unique() if x != "Unknown"])

    min_year, max_year = int(df.release_year.min()), int(df.release_year.max())



    selected_type = st.selectbox("Type", types, key="type_filter")

    selected_country = st.selectbox("Country", countries, key="country_filter")

    selected_genre = st.selectbox("Genre", genres, key="genre_filter")

    year_range = st.slider("Release Year", min_year, max_year, (min_year, max_year), key="year_filter")

    selected_rating = st.selectbox("Rating", ratings, key="rating_filter")

    if st.button("↻  Reset Filters", use_container_width=True):

        reset_filters()

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)



# -----------------------------

# Filtering

# -----------------------------

filtered = df.copy()

if selected_type != "All":

    filtered = filtered[filtered.type == selected_type]

if selected_country != "All":

    filtered = filtered[filtered.country_primary == selected_country]

if selected_genre != "All":

    filtered = filtered[filtered.listed_in_primary == selected_genre]

if selected_rating != "All":

    filtered = filtered[filtered.rating == selected_rating]

filtered = filtered[filtered.release_year.between(year_range[0], year_range[1])]



# -----------------------------

# Plot helpers

# -----------------------------

RED = "#F61F35"

PINK = "#ff9aa0"

GRID = "#252a30"

TEXT = "#e9eaed"

BG = "rgba(0,0,0,0)"





def style_fig(fig, height=320):

    fig.update_layout(

        template="plotly_dark", height=height, paper_bgcolor=BG, plot_bgcolor=BG,

        font=dict(color=TEXT, family="Arial"), margin=dict(l=8, r=12, t=52, b=12),

        title=dict(font=dict(size=17, color="#fff")), legend=dict(bgcolor="rgba(0,0,0,0)"),

        hoverlabel=dict(bgcolor="#171a1e", font_color="#fff"),

    )

    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID)

    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID)

    return fig





def page_head(title, subtitle):

    st.markdown(f'<div class="page-head"><div><div class="page-title">{title}</div><div class="page-subtitle">{subtitle}</div></div><div><span class="pill">{len(filtered):,} filtered titles</span></div></div>', unsafe_allow_html=True)





def kpi_card(label, value, icon_name, trend=True):

    data = kpi_icon(icon_name)

    trend_html = '<div class="kpi-trend">⌁</div>' if trend else ''

    return f'<div class="kpi-card"><img class="kpi-icon" src="{data}"><div><div class="kpi-label">{label}</div><div class="kpi-value">{value:,}</div></div>{trend_html}</div>'





def metric(label, value):

    return f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>'





def show_posters(items):

    cols = st.columns(len(items))

    for col, item in zip(cols, items):

        with col:

            data = img64(asset("posters", item["poster"]))

            if data:

                st.markdown(f'<div class="poster-card"><img src="{data}"><div class="poster-title">{item["title"]}</div><div class="poster-meta">{item["type"]} &nbsp; <span class="rating">★</span> {item["rating"]}</div></div>', unsafe_allow_html=True)





def top_posters():

    return [

        {"title":"Inception","type":"Movie","rating":"8.8","poster":"top_inception.png"},

        {"title":"Breaking Bad","type":"TV Show","rating":"9.5","poster":"thumb_breakingbad.png"},

        {"title":"The Dark Knight","type":"Movie","rating":"9.0","poster":"top_dark_knight.png"},

        {"title":"Stranger Things","type":"TV Show","rating":"8.7","poster":"top_stranger_things.png"},

        {"title":"Interstellar","type":"Movie","rating":"8.6","poster":"thumb_interstellar.png"},

        {"title":"Money Heist","type":"TV Show","rating":"8.2","poster":"top_money_heist.png"},

    ]





def catalog_table(data, height=430):

    cols = ["title", "type", "release_year", "rating", "country_primary", "listed_in_primary", "duration"]

    table = data[cols].sort_values(["release_year", "title"], ascending=[False, True])

    st.dataframe(table, use_container_width=True, hide_index=True, height=height)



# -----------------------------

# Pages

# -----------------------------

def render_home():

    hero = img64(asset("hero", "netflix_analytics_hero.jpg"))

    st.markdown(f'<div class="hero" style="background-image:url({hero})"><div class="hero-overlay"><div class="hero-copy"><div class="hero-kicker">DATA ANALYSIS</div><div class="hero-title">NETFLIX<span>ANALYTICS</span></div><p>Explore movies and TV shows from around the world and discover insights from Netflix\'s extensive catalog.</p><div class="hero-btn">Explore Insights &nbsp; →</div></div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)



    cols = st.columns(5)

    cards = [

        ("Total Titles", len(filtered), "titles.png"),

        ("Movies", int((filtered.type == "Movie").sum()), "movies.png"),

        ("TV Shows", int((filtered.type == "TV Show").sum()), "tv_shows.png"),

        ("Countries", filtered.country_primary.nunique(), "countries.png"),

        ("Ratings", filtered.rating.nunique(), "ratings.png"),

    ]

    for col, (label, value, ic) in zip(cols, cards):

        col.markdown(kpi_card(label, value, ic), unsafe_allow_html=True)



    st.markdown('<div class="section-title">Catalog at a glance</div>', unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:

        x = filtered.type.value_counts().reset_index(); x.columns = ["Type", "Titles"]

        fig = px.pie(x, names="Type", values="Titles", hole=.58, color="Type", color_discrete_map={"Movie": RED, "TV Show": PINK}, title="Content by Type")

        st.plotly_chart(style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})

    with b:

        co = filtered.country_primary.value_counts().head(10).sort_values().reset_index(); co.columns = ["Country", "Titles"]

        fig = px.bar(co, x="Titles", y="Country", orientation="h", text="Titles", title="Top 10 Countries", color_discrete_sequence=[RED])

        fig.update_traces(textposition="outside", cliponaxis=False)

        st.plotly_chart(style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})

    with c:

        y = filtered.dropna(subset=["date_added"]).groupby(filtered.dropna(subset=["date_added"])["date_added"].dt.year).size().reset_index(name="Titles")

        y.columns = ["Year", "Titles"]

        fig = px.line(y, x="Year", y="Titles", markers=True, title="Titles Added Over Time")

        fig.update_traces(line=dict(color=RED, width=3), fill="tozeroy", fillcolor="rgba(229,9,20,.15)")

        st.plotly_chart(style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})



    st.markdown('<div class="section-title">Genres & Top Rated Titles</div>', unsafe_allow_html=True)

    a, b = st.columns([1.05, 1.55])

    with a:

        g = filtered.listed_in_primary.value_counts().head(10).sort_values().reset_index(); g.columns = ["Genre", "Titles"]

        fig = px.bar(g, x="Titles", y="Genre", orientation="h", title="Top Genres", color_discrete_sequence=[RED])

        st.plotly_chart(style_fig(fig, 315), use_container_width=True, config={"displayModeBar": False})

    with b:

        show_posters(top_posters())





def render_overview():

    page_head("Overview", "A high-level view of catalog composition, audience ratings, geography and time.")

    cols = st.columns(5)

    cards = [("Total Titles", len(filtered), "titles.png"), ("Movies", int((filtered.type == "Movie").sum()), "movies.png"), ("TV Shows", int((filtered.type == "TV Show").sum()), "tv_shows.png"), ("Countries", filtered.country_primary.nunique(), "countries.png"), ("Genres", filtered.listed_in_primary.nunique(), "ratings.png")]

    for col, item in zip(cols, cards): col.markdown(kpi_card(*item), unsafe_allow_html=True)



    a, b = st.columns(2)

    with a:

        x = filtered.type.value_counts().reset_index(); x.columns = ["Type", "Titles"]

        fig = px.pie(x, names="Type", values="Titles", hole=.5, color="Type", color_discrete_map={"Movie": RED, "TV Show": PINK}, title="Movie vs TV Show Mix")

        st.plotly_chart(style_fig(fig, 330), use_container_width=True)

    with b:

        r = filtered.rating.value_counts().head(12).reset_index(); r.columns = ["Rating", "Titles"]

        fig = px.bar(r, x="Rating", y="Titles", title="Most Common Ratings", color_discrete_sequence=[RED], text="Titles")

        fig.update_traces(textposition="outside")

        st.plotly_chart(style_fig(fig, 330), use_container_width=True)



    a, b = st.columns(2)

    with a:

        y = filtered.release_year.value_counts().sort_index().reset_index(); y.columns = ["Release Year", "Titles"]

        fig = px.area(y, x="Release Year", y="Titles", title="Catalog by Release Year", color_discrete_sequence=[RED])

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    with b:

        m = filtered.dropna(subset=["date_added"]).groupby(filtered.dropna(subset=["date_added"])["date_added"].dt.month_name()).size().reset_index(name="Titles")

        order = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        m.columns = ["Month", "Titles"]; m["Month"] = pd.Categorical(m["Month"], categories=order, ordered=True); m = m.sort_values("Month")

        fig = px.bar(m, x="Month", y="Titles", title="Titles Added by Month", color_discrete_sequence=[PINK])

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)



    a, b = st.columns(2)

    with a:

        co = filtered.country_primary.value_counts().head(12).sort_values().reset_index(); co.columns = ["Country", "Titles"]

        fig = px.bar(co, x="Titles", y="Country", orientation="h", title="Top Countries", color_discrete_sequence=[RED])

        st.plotly_chart(style_fig(fig, 400), use_container_width=True)

    with b:

        g = filtered.listed_in_primary.value_counts().head(12).sort_values().reset_index(); g.columns = ["Genre", "Titles"]

        fig = px.bar(g, x="Titles", y="Genre", orientation="h", title="Top Genres", color_discrete_sequence=[PINK])

        st.plotly_chart(style_fig(fig, 400), use_container_width=True)





def render_movies():

    data = filtered[filtered.type == "Movie"].copy()

    page_head("Movies", "Explore the movie catalog by release year, genre, country, rating and duration.")

    avg_duration = data.duration_value.mean() if not data.empty else 0

    common_genre = data.listed_in_primary.mode().iat[0] if not data.empty else "—"

    common_rating = data.rating.mode().iat[0] if not data.empty else "—"

    cols = st.columns(4)

    for col, item in zip(cols, [("Movies", len(data), "movies.png"), ("Avg Duration", f"{avg_duration:.0f} min" if avg_duration else "—", "titles.png"), ("Top Genre", common_genre, "ratings.png"), ("Top Rating", common_rating, "ratings.png")]):

        if isinstance(item[1], int): col.markdown(kpi_card(item[0], item[1], item[2]), unsafe_allow_html=True)

        else: col.markdown(metric(item[0], item[1]), unsafe_allow_html=True)



    a, b = st.columns(2)

    with a:

        y = data.release_year.value_counts().sort_index().reset_index(); y.columns = ["Year", "Movies"]

        fig = px.line(y, x="Year", y="Movies", markers=True, title="Movies by Release Year")

        fig.update_traces(line=dict(color=RED, width=3), fill="tozeroy", fillcolor="rgba(229,9,20,.13)")

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    with b:

        g = data.listed_in_primary.value_counts().head(12).sort_values().reset_index(); g.columns = ["Genre", "Movies"]

        fig = px.bar(g, x="Movies", y="Genre", orientation="h", title="Top Movie Genres", color_discrete_sequence=[RED])

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)



    a, b = st.columns(2)

    with a:

        co = data.country_primary.value_counts().head(12).sort_values().reset_index(); co.columns = ["Country", "Movies"]

        fig = px.bar(co, x="Movies", y="Country", orientation="h", title="Movie Production Countries", color_discrete_sequence=[PINK])

        st.plotly_chart(style_fig(fig, 360), use_container_width=True)

    with b:

        r = data.rating.value_counts().reset_index(); r.columns = ["Rating", "Movies"]

        fig = px.bar(r, x="Rating", y="Movies", title="Movie Rating Distribution", color_discrete_sequence=[RED], text="Movies")

        fig.update_traces(textposition="outside")

        st.plotly_chart(style_fig(fig, 360), use_container_width=True)



    st.markdown('<div class="section-title">Movie Duration Distribution</div>', unsafe_allow_html=True)

    dur = data.dropna(subset=["duration_value"])

    if not dur.empty:

        fig = px.histogram(dur, x="duration_value", nbins=30, title="Movie Runtime in Minutes", color_discrete_sequence=[RED])

        fig.update_xaxes(title="Minutes"); fig.update_yaxes(title="Movies")

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    st.markdown('<div class="section-title">Movie Catalog</div>', unsafe_allow_html=True)

    catalog_table(data)





def render_tv():

    data = filtered[filtered.type == "TV Show"].copy()

    page_head("TV Shows", "Explore series by release year, genres, countries, ratings and number of seasons.")

    avg_seasons = data.duration_value.mean() if not data.empty else 0

    common_genre = data.listed_in_primary.mode().iat[0] if not data.empty else "—"

    common_rating = data.rating.mode().iat[0] if not data.empty else "—"

    cols = st.columns(4)

    for col, item in zip(cols, [("TV Shows", len(data), "tv_shows.png"), ("Avg Seasons", f"{avg_seasons:.1f}" if avg_seasons else "—", "titles.png"), ("Top Genre", common_genre, "ratings.png"), ("Top Rating", common_rating, "ratings.png")]):

        if isinstance(item[1], int): col.markdown(kpi_card(item[0], item[1], item[2]), unsafe_allow_html=True)

        else: col.markdown(metric(item[0], item[1]), unsafe_allow_html=True)



    a, b = st.columns(2)

    with a:

        y = data.release_year.value_counts().sort_index().reset_index(); y.columns = ["Year", "TV Shows"]

        fig = px.line(y, x="Year", y="TV Shows", markers=True, title="TV Shows by Release Year")

        fig.update_traces(line=dict(color=RED, width=3), fill="tozeroy", fillcolor="rgba(229,9,20,.13)")

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    with b:

        g = data.listed_in_primary.value_counts().head(12).sort_values().reset_index(); g.columns = ["Genre", "TV Shows"]

        fig = px.bar(g, x="TV Shows", y="Genre", orientation="h", title="Top TV Show Genres", color_discrete_sequence=[PINK])

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)



    a, b = st.columns(2)

    with a:

        co = data.country_primary.value_counts().head(12).sort_values().reset_index(); co.columns = ["Country", "TV Shows"]

        fig = px.bar(co, x="TV Shows", y="Country", orientation="h", title="TV Show Countries", color_discrete_sequence=[RED])

        st.plotly_chart(style_fig(fig, 360), use_container_width=True)

    with b:

        r = data.rating.value_counts().reset_index(); r.columns = ["Rating", "TV Shows"]

        fig = px.bar(r, x="Rating", y="TV Shows", title="TV Show Rating Distribution", color_discrete_sequence=[PINK], text="TV Shows")

        fig.update_traces(textposition="outside")

        st.plotly_chart(style_fig(fig, 360), use_container_width=True)



    st.markdown('<div class="section-title">Seasons Distribution</div>', unsafe_allow_html=True)

    seasons = data.dropna(subset=["duration_value"]).copy()

    if not seasons.empty:

        seasons["Seasons"] = seasons["duration_value"].astype(int).astype(str)

        s = seasons["Seasons"].value_counts().sort_index().reset_index(); s.columns = ["Seasons", "Shows"]

        fig = px.bar(s, x="Seasons", y="Shows", title="Number of Seasons per Show", color_discrete_sequence=[RED], text="Shows")

        fig.update_traces(textposition="outside")

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    st.markdown('<div class="section-title">TV Show Catalog</div>', unsafe_allow_html=True)

    catalog_table(data)





def render_countries():

    page_head("Countries", "Compare Netflix catalog coverage across countries and content types.")

    country = filtered.country_primary.replace("Unknown", pd.NA).dropna()

    top = country.value_counts().head(15).index.tolist()

    data = filtered[filtered.country_primary.isin(top)].copy()

    a, b = st.columns(2)

    with a:

        co = data.country_primary.value_counts().sort_values().reset_index(); co.columns = ["Country", "Titles"]

        fig = px.bar(co, x="Titles", y="Country", orientation="h", title="Top 15 Countries by Titles", color_discrete_sequence=[RED], text="Titles")

        fig.update_traces(textposition="outside")

        st.plotly_chart(style_fig(fig, 470), use_container_width=True)

    with b:

        mix = data.groupby(["country_primary", "type"]).size().reset_index(name="Titles")

        fig = px.bar(mix, x="country_primary", y="Titles", color="type", barmode="group", title="Movies vs TV Shows by Country", color_discrete_map={"Movie": RED, "TV Show": PINK})

        fig.update_xaxes(tickangle=-35)

        st.plotly_chart(style_fig(fig, 470), use_container_width=True)



    a, b = st.columns(2)

    with a:

        g = data.groupby("country_primary")["listed_in_primary"].nunique().sort_values(ascending=False).head(15).sort_values().reset_index(); g.columns = ["Country", "Genres"]

        fig = px.bar(g, x="Genres", y="Country", orientation="h", title="Genre Variety by Country", color_discrete_sequence=[PINK])

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with b:

        years = data.dropna(subset=["date_added"]).groupby([data.dropna(subset=["date_added"])["date_added"].dt.year, "type"]).size().reset_index(name="Titles")

        years.columns = ["Year", "Type", "Titles"]

        fig = px.line(years, x="Year", y="Titles", color="Type", markers=True, title="Country Group Additions Over Time", color_discrete_map={"Movie": RED, "TV Show": PINK})

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)



    st.markdown('<div class="section-title">Country Details</div>', unsafe_allow_html=True)

    summary = data.groupby("country_primary").agg(Titles=("show_id", "count"), Movies=("type", lambda s: (s == "Movie").sum()), TV_Shows=("type", lambda s: (s == "TV Show").sum()), Genres=("listed_in_primary", "nunique")).reset_index().sort_values("Titles", ascending=False)

    st.dataframe(summary, use_container_width=True, hide_index=True, height=330)





def render_genres():

    page_head("Genres", "See which genres dominate the catalog and how their content mix differs.")

    gcounts = filtered.listed_in_primary.value_counts().head(15)

    a, b = st.columns(2)

    with a:

        g = gcounts.sort_values().reset_index(); g.columns = ["Genre", "Titles"]

        fig = px.bar(g, x="Titles", y="Genre", orientation="h", title="Top 15 Genres", color_discrete_sequence=[RED], text="Titles")

        fig.update_traces(textposition="outside")

        st.plotly_chart(style_fig(fig, 470), use_container_width=True)

    with b:

        mix = filtered[filtered.listed_in_primary.isin(gcounts.index)].groupby(["listed_in_primary", "type"]).size().reset_index(name="Titles")

        fig = px.bar(mix, x="listed_in_primary", y="Titles", color="type", barmode="group", title="Movies vs TV Shows by Genre", color_discrete_map={"Movie": RED, "TV Show": PINK})

        fig.update_xaxes(tickangle=-40)

        st.plotly_chart(style_fig(fig, 470), use_container_width=True)



    a, b = st.columns(2)

    with a:

        trend = filtered[filtered.listed_in_primary.isin(gcounts.head(6).index)].dropna(subset=["date_added"]).copy()

        trend["Year"] = trend["date_added"].dt.year

        trend = trend.groupby(["Year", "listed_in_primary"]).size().reset_index(name="Titles")

        fig = px.line(trend, x="Year", y="Titles", color="listed_in_primary", markers=True, title="Top Genre Additions Over Time")

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with b:

        country_genre = filtered.groupby("listed_in_primary")["country_primary"].nunique().sort_values(ascending=False).head(12).sort_values().reset_index(); country_genre.columns = ["Genre", "Countries"]

        fig = px.bar(country_genre, x="Countries", y="Genre", orientation="h", title="Genre Geographic Reach", color_discrete_sequence=[PINK])

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)



    st.markdown('<div class="section-title">Genre Details</div>', unsafe_allow_html=True)

    details = filtered.groupby("listed_in_primary").agg(Titles=("show_id", "count"), Countries=("country_primary", "nunique"), Avg_Release_Year=("release_year", "mean")).reset_index().sort_values("Titles", ascending=False)

    details["Avg_Release_Year"] = details["Avg_Release_Year"].round(1)

    st.dataframe(details, use_container_width=True, hide_index=True, height=350)





def render_ratings():

    page_head("Ratings", "Understand the maturity-rating mix and how ratings vary across Movies and TV Shows.")

    a, b = st.columns(2)

    with a:

        r = filtered.rating.value_counts().reset_index(); r.columns = ["Rating", "Titles"]

        fig = px.bar(r, x="Rating", y="Titles", title="Rating Distribution", color_discrete_sequence=[RED], text="Titles")

        fig.update_traces(textposition="outside")

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with b:

        mix = filtered.groupby(["rating", "type"]).size().reset_index(name="Titles")

        fig = px.bar(mix, x="rating", y="Titles", color="type", barmode="group", title="Ratings by Content Type", color_discrete_map={"Movie": RED, "TV Show": PINK})

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)



    a, b = st.columns(2)

    with a:

        trend = filtered.dropna(subset=["date_added"]).groupby([filtered.dropna(subset=["date_added"])["date_added"].dt.year, "rating"]).size().reset_index(name="Titles")

        trend.columns = ["Year", "Rating", "Titles"]

        top_r = filtered.rating.value_counts().head(6).index

        trend = trend[trend.Rating.isin(top_r)]

        fig = px.line(trend, x="Year", y="Titles", color="Rating", markers=True, title="Top Ratings Added Over Time")

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with b:

        avg_year = filtered.groupby("rating")["release_year"].mean().sort_values(ascending=False).reset_index(); avg_year.columns = ["Rating", "Avg Release Year"]

        avg_year["Avg Release Year"] = avg_year["Avg Release Year"].round(1)

        fig = px.bar(avg_year, x="Rating", y="Avg Release Year", title="Average Release Year by Rating", color_discrete_sequence=[PINK])

        st.plotly_chart(style_fig(fig, 430), use_container_width=True)



    st.markdown('<div class="section-title">Rating Details</div>', unsafe_allow_html=True)

    details = filtered.groupby("rating").agg(Titles=("show_id", "count"), Movies=("type", lambda s: (s == "Movie").sum()), TV_Shows=("type", lambda s: (s == "TV Show").sum()), Avg_Release_Year=("release_year", "mean")).reset_index().sort_values("Titles", ascending=False)

    details["Avg_Release_Year"] = details["Avg_Release_Year"].round(1)

    st.dataframe(details, use_container_width=True, hide_index=True, height=330)





def render_trends():

    page_head("Trends", "Track catalog growth, additions, and the changing balance between Movies and TV Shows.")

    added = filtered.dropna(subset=["date_added"]).copy()

    added["Year"] = added["date_added"].dt.year

    yearly = added.groupby("Year").size().reset_index(name="Titles")

    a, b = st.columns(2)

    with a:

        fig = px.line(yearly, x="Year", y="Titles", markers=True, title="Titles Added by Year")

        fig.update_traces(line=dict(color=RED, width=4), fill="tozeroy", fillcolor="rgba(229,9,20,.14)")

        st.plotly_chart(style_fig(fig, 380), use_container_width=True)

    with b:

        by_type = added.groupby(["Year", "type"]).size().reset_index(name="Titles")

        fig = px.area(by_type, x="Year", y="Titles", color="type", title="Movie vs TV Additions", color_discrete_map={"Movie": RED, "TV Show": PINK})

        st.plotly_chart(style_fig(fig, 380), use_container_width=True)



    a, b = st.columns(2)

    with a:

        monthly = added.groupby(added["date_added"].dt.to_period("M").astype(str)).size().reset_index(name="Titles")

        monthly.columns = ["Month", "Titles"]

        fig = px.bar(monthly.tail(36), x="Month", y="Titles", title="Monthly Additions — Last 36 Months", color_discrete_sequence=[RED])

        fig.update_xaxes(tickangle=-45)

        st.plotly_chart(style_fig(fig, 400), use_container_width=True)

    with b:

        release = filtered.release_year.value_counts().sort_index().reset_index(); release.columns = ["Release Year", "Titles"]

        fig = px.line(release, x="Release Year", y="Titles", markers=True, title="Release-Year Profile")

        fig.update_traces(line=dict(color=PINK, width=3))

        st.plotly_chart(style_fig(fig, 400), use_container_width=True)



    st.markdown('<div class="section-title">Yearly Growth</div>', unsafe_allow_html=True)

    # -----------------------------
    # Growth KPIs
    # -----------------------------

    growth = yearly.copy()
    growth["YoY Change %"] = growth["Titles"].pct_change().mul(100)

    latest = growth.iloc[-1] if not growth.empty else None
    peak_row = growth.loc[growth["Titles"].idxmax()] if not growth.empty else None

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            metric(
                "Latest Year",
                f'{int(latest["Year"])}' if latest is not None else "—"
            ),
            unsafe_allow_html=True
        )

    with k2:
        st.markdown(
            metric(
                "Latest Titles",
                f'{int(latest["Titles"]):,}' if latest is not None else "—"
            ),
            unsafe_allow_html=True
        )

    with k3:
        latest_growth = latest["YoY Change %"] if latest is not None else None
        growth_value = "—" if pd.isna(latest_growth) else f"{latest_growth:+.1f}%"

        st.markdown(
            metric("YoY Growth", growth_value),
            unsafe_allow_html=True
        )

    with k4:
        st.markdown(
            metric(
                "Peak Year",
                f'{int(peak_row["Year"])}' if peak_row is not None else "—"
            ),
            unsafe_allow_html=True
        )

    # -----------------------------
    # Main Growth Charts
    # -----------------------------

    a, b = st.columns(2)

    with a:
        fig = px.area(
            growth,
            x="Year",
            y="Titles",
            title="Titles Added by Year",
            color_discrete_sequence=[RED]
        )

        fig.update_traces(
            line=dict(color=RED, width=3),
            fillcolor="rgba(246,31,53,.16)"
        )

        st.plotly_chart(
            style_fig(fig, 360),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with b:
        growth_chart = growth.dropna(subset=["YoY Change %"]).copy()

        fig = px.bar(
            growth_chart,
            x="Year",
            y="YoY Change %",
            title="Year-over-Year Growth",
            color_discrete_sequence=[PINK],
            text="YoY Change %"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            cliponaxis=False
        )

        fig.add_hline(
            y=0,
            line_width=1,
            line_color="#555"
        )

        st.plotly_chart(
            style_fig(fig, 360),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # -----------------------------
    # Recent Years
    # -----------------------------

    st.markdown(
        '<div class="section-title">Recent Years</div>',
        unsafe_allow_html=True
    )

    recent = growth.tail(6).copy()
    cols = st.columns(max(1, len(recent)))

    for col, (_, row) in zip(cols, recent.iterrows()):
        yoy = row["YoY Change %"]

        if pd.isna(yoy):
            change = "—"
        elif yoy >= 0:
            change = f"↑ {yoy:.1f}%"
        else:
            change = f"↓ {abs(yoy):.1f}%"

        col.markdown(
            f'''
            <div class="metric-box growth-year-card">
                <div class="metric-label">{int(row["Year"])}</div>
                <div class="metric-value">{int(row["Titles"]):,}</div>
                <div class="growth-change">{change}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )


def render_filters():

    page_head("Filters", "Build your own slice of the Netflix catalog and inspect the matching records.")

    a, b, c, d = st.columns(4)

    a.markdown(metric("Matching Titles", f"{len(filtered):,}"), unsafe_allow_html=True)

    b.markdown(metric("Countries", f"{filtered.country_primary.nunique():,}"), unsafe_allow_html=True)

    c.markdown(metric("Genres", f"{filtered.listed_in_primary.nunique():,}"), unsafe_allow_html=True)

    d.markdown(metric("Ratings", f"{filtered.rating.nunique():,}"), unsafe_allow_html=True)



    a, b = st.columns(2)

    with a:

        x = filtered.type.value_counts().reset_index(); x.columns = ["Type", "Titles"]

        fig = px.pie(x, names="Type", values="Titles", hole=.55, title="Filtered Content Mix", color="Type", color_discrete_map={"Movie": RED, "TV Show": PINK})

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    with b:

        y = filtered.release_year.value_counts().sort_index().reset_index(); y.columns = ["Year", "Titles"]

        fig = px.line(y, x="Year", y="Titles", markers=True, title="Filtered Titles by Release Year")

        fig.update_traces(line=dict(color=RED, width=3))

        st.plotly_chart(style_fig(fig, 350), use_container_width=True)



    st.markdown('<div class="section-title">Filtered Results</div>', unsafe_allow_html=True)

    export = filtered[["show_id","title","type","director","country","date_added","release_year","rating","duration","listed_in","description"]].copy()

    csv = export.to_csv(index=False).encode("utf-8")

    st.download_button("⬇ Download Filtered CSV", data=csv, file_name="netflix_filtered.csv", mime="text/csv")

    catalog_table(filtered, 520)



# -----------------------------

# Router

# -----------------------------

page = st.session_state.page

if page == "Home": render_home()

elif page == "Overview": render_overview()

elif page == "Movies": render_movies()

elif page == "TV Shows": render_tv()

elif page == "Countries": render_countries()

elif page == "Genres": render_genres()

elif page == "Ratings": render_ratings()

elif page == "Trends": render_trends()

elif page == "Filters": render_filters()

# -----------------------------
# Copyright
# -----------------------------
st.markdown(
    """
    <div class="copyright">
        © 2026 <strong>Noura Maher</strong>. All Rights Reserved.
        <span> | </span>
        <a href="https://github.com/nouramaherelamin" target="_blank">GitHub</a>
        <span> · </span>
        <a href="https://www.linkedin.com/in/nouramaherelamin/" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
