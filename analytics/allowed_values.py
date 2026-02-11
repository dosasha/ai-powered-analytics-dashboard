import pandas as pd
import json
import os

# Define paths relative to this script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONTHLY_REV_PATH = os.path.join(BASE_DIR, "../data/processed/monthly_revenue.csv")
COUNTRY_REV_PATH = os.path.join(BASE_DIR, "../data/processed/country_revenue.csv")
OUT_PATH = os.path.join(BASE_DIR, "../data/processed/metadata.json")

def main():
    print("Extracting allowed values for validation...")
    
    metadata = {
        "allowed_yearmonths": [],
        "allowed_countries": [],
        "capabilities": {
            "modes": ["overall", "month_focus"],
            "slots": [
                "slot_kpi_cards",
                "slot_trend",
                "slot_top_countries",
                "slot_top_products"
            ],
            "metrics": ["revenue"]
        }
    }

    # 1. Extract YearMonths
    if os.path.exists(MONTHLY_REV_PATH):
        try:
            df_month = pd.read_csv(MONTHLY_REV_PATH)
            # Ensure YearMonth is string and sort
            months = sorted(df_month["YearMonth"].astype(str).unique().tolist())
            metadata["allowed_yearmonths"] = months
            print(f"Loaded {len(months)} allowed YearMonths.")
        except Exception as e:
            print(f"Error reading monthly revenue: {e}")
    else:
        print(f"Warning: {MONTHLY_REV_PATH} not found.")

    # 2. Extract Countries
    if os.path.exists(COUNTRY_REV_PATH):
        try:
            df_country = pd.read_csv(COUNTRY_REV_PATH)
            countries = sorted(df_country["Country"].astype(str).unique().tolist())
            metadata["allowed_countries"] = countries
            print(f"Loaded {len(countries)} allowed Countries.")
        except Exception as e:
            print(f"Error reading country revenue: {e}")
    else:
        print(f"Warning: {COUNTRY_REV_PATH} not found.")

    # Save to JSON
    with open(OUT_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Saved metadata to {OUT_PATH}")
    # Print preview
    print(json.dumps(metadata, indent=2)[:500] + "...")

if __name__ == "__main__":
    main()
