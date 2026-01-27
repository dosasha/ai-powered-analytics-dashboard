import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

MONTHLY = BASE_DIR / "data" / "processed" / "monthly_revenue.csv"
COUNTRY = BASE_DIR / "data" / "processed" / "country_revenue.csv"
TOP = BASE_DIR / "data" / "processed" / "top_products.csv"

def load_csv(path):
    return pd.read_csv(path, low_memory=False)

def package_for_llm(period=None):
    monthly = load_csv(MONTHLY)
    country = load_csv(COUNTRY)
    top = load_csv(TOP)

    evidence = {
        "monthly_head": monthly.head(6).to_dict(orient="records"),
        "top_countries": country.head(5).to_dict(orient="records"),
        "top_products": top.head(5).to_dict(orient="records"),
    }
    return evidence

if __name__ == "__main__":
    print(package_for_llm())