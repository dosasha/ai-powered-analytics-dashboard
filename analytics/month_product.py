import pandas as pd
import os

# Define paths relative to this script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/processed/online_retail_cleaned.csv")
OUT_PATH = os.path.join(BASE_DIR, "../data/processed/month_product_revenue.csv")
TOP_N = 50

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

    print("Aggregating Revenue by YearMonth and Product Description...")
    # Group by [YearMonth, Description] and sum Revenue
    month_product_df = (
        df.groupby(["YearMonth", "Description"])["Revenue"]
        .sum()
        .reset_index()
    )

    print(f"Filtering to Top {TOP_N} products per month...")
    # Sort by YearMonth and Revenue (Desc)
    month_product_df = month_product_df.sort_values(by=["YearMonth", "Revenue"], ascending=[True, False])

    # Keep only top N per month
    top_products_monthly = month_product_df.groupby("YearMonth").head(TOP_N)

    # Save
    print(f"Saving {len(top_products_monthly)} rows to {OUT_PATH}...")
    top_products_monthly.to_csv(OUT_PATH, index=False)
    
    print("Top 5 rows:")
    print(top_products_monthly.head())
    print("\nSuccess.")

if __name__ == "__main__":
    main()
