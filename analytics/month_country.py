import pandas as pd
import os

# Define paths relative to this script location for robust execution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/processed/online_retail_cleaned.csv")
OUT_PATH = os.path.join(BASE_DIR, "../data/processed/month_country_revenue.csv")

def main():
    print("Loading data from:", DATA_PATH)
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: File not found at {DATA_PATH}")
        return

    # Ensure InvoiceDate is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["InvoiceDate"]):
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Create YearMonth column (YYYY-MM)
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    # Group by YearMonth and Country, summing Revenue
    print("Aggregating Revenue by YearMonth and Country...")
    month_country_df = (
        df.groupby(["YearMonth", "Country"])["Revenue"]
        .sum()
        .reset_index()
    )

    # Sort primarily by YearMonth (chronological), secondarily by Revenue (descending)
    # This helps finding 'top countries' for a month easily
    month_country_df = month_country_df.sort_values(by=["YearMonth", "Revenue"], ascending=[True, False])

    # Save to CSV
    print(f"Saving {len(month_country_df)} rows to {OUT_PATH}...")
    month_country_df.to_csv(OUT_PATH, index=False)
    
    print("Top 5 rows:")
    print(month_country_df.head())
    print("\nSuccess.")

if __name__ == "__main__":
    main()
