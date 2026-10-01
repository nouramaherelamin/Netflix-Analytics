import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    out=df.copy()
    for c in ["director","cast","country","date_added","rating","duration"]:
        out[c]=out[c].fillna("Unknown")
    out["date_added"]=pd.to_datetime(out["date_added"], errors="coerce")
    out["year_added"]=out["date_added"].dt.year
    out["listed_in_primary"]=out["listed_in"].fillna("Unknown").str.split(",").str[0].str.strip()
    out["country_primary"]=out["country"].fillna("Unknown").str.split(",").str[0].str.strip()
    out["duration_value"]=pd.to_numeric(out["duration"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
    return out

def kpis(df):
    return {"total_titles":len(df),"movies":int((df.type=="Movie").sum()),"tv_shows":int((df.type=="TV Show").sum()),"countries":df.country_primary.nunique()}
