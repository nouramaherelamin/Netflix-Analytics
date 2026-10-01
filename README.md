# Netflix Analytics Dashboard

A dark, Netflix-inspired interactive analytics dashboard built with
**Python, Pandas, Plotly, and Streamlit** to explore Netflix movies and
TV shows through KPIs, filters, trends, ratings, genres, countries, and
content-type analysis.

## Project Description

Netflix Analytics is an interactive data analysis project based on the
Netflix titles catalog. It transforms the raw dataset into a clean
analytical dataset and presents the findings through a multi-page
Streamlit dashboard with a consistent Netflix-inspired visual identity.

## Features

-   Interactive Streamlit dashboard
-   Netflix-inspired dark/red UI
-   Global filters for content type, country, genre, release year, and
    rating
-   Interactive KPIs and visualizations
-   Movies and TV Shows analysis
-   Country and genre analysis
-   Ratings analysis
-   Release and catalog trends
-   Top-rated title showcase
-   Filtered-data CSV download
-   Final Jupyter Notebook
-   Reusable Python analysis module
-   Project report and generated figures
-   Custom high-quality UI icons and visual assets

## Dashboard Destinations

1.  **Home** --- Hero section, KPIs, content mix, top countries, title
    additions, genres, and top-rated titles.
2.  **Overview** --- Catalog composition, ratings, release-year profile,
    monthly additions, countries, and genres.
3.  **Movies** --- Movie KPIs, release trends, genres, countries,
    ratings, runtime distribution, and movie catalog.
4.  **TV Shows** --- TV-specific KPIs, release trends, genres,
    countries, ratings, season distribution, and TV catalog.
5.  **Countries** --- Country rankings, Movies vs TV Shows, genre
    variety, additions over time, and country details.
6.  **Genres** --- Top genres, Movies vs TV Shows by genre, genre
    trends, geographic reach, and genre details.
7.  **Ratings** --- Rating distribution, content-type comparison, rating
    trends, and release-year analysis.
8.  **Trends** --- Yearly additions, Movies vs TV additions, monthly
    additions, and release-year trends.
9.  **Filters** --- Interactive filtering, filtered KPIs, charts,
    detailed records, and CSV export.

## Project Structure

``` text
Netflix_Analytics_Final/
├── app/
│   ├── app.py
│   └── run_app.bat
├── assets/
│   ├── backgrounds/
│   ├── branding/
│   ├── icons/
│   ├── kpi/
│   ├── posters/
│   └── hero/
├── data/
│   ├── raw/
│   └── processed/
├── figures/
├── notebooks/
│   └── Netflix_Analytics_Final.ipynb
├── reports/
│   ├── FINAL_REPORT.md
│   └── summary.json
├── src/
│   └── analysis.py
├── tests/
│   └── test_analysis.py
├── requirements.txt
└── README.md
```

## Installation

Open a terminal inside the project folder.

If `pip` is not recognized on Windows:

``` bash
py -m pip install -r requirements.txt
```

Otherwise:

``` bash
pip install -r requirements.txt
```

## Run the Dashboard

``` bash
py -m streamlit run app/app.py
```

Or on Windows, double-click:

``` text
app/run_app.bat
```

The dashboard will normally be available at:

``` text
http://localhost:8501
```

## Run the Tests

``` bash
python -m pytest -q
```

The project includes automated tests for the analysis module.

## Technologies

-   Python
-   Pandas
-   Plotly
-   Streamlit
-   Jupyter Notebook
-   Pytest

## Data

The project uses the Netflix titles dataset and includes both the
original raw CSV and a cleaned processed version.

The analytical workflow includes data cleaning, transformation,
exploratory analysis, visualization, and interactive dashboard
presentation.

## UI & Branding

The dashboard uses a dark cinema-inspired interface with Netflix-style
red accents. The provided **512×512 transparent PNG icon pack** is used
throughout the navigation and dashboard UI.

## Author

**Noura Maher**

Data Analysis \| Machine Learning \| Data Engineering
