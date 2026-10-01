import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.analysis import load_data, clean_data, kpis

def test_load_and_clean():
    p=Path(__file__).resolve().parents[1]/'data/raw/netflix_titles.csv'
    df=clean_data(load_data(p))
    assert len(df)==8807
    assert 'year_added' in df.columns

def test_kpis():
    p=Path(__file__).resolve().parents[1]/'data/raw/netflix_titles.csv'
    k=kpis(clean_data(load_data(p)))
    assert k['total_titles']==8807
    assert k['movies']>k['tv_shows']
