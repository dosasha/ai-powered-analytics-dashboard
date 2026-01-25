import pandas as pd

DATA_PATH = "data/processed/online_retail_cleaned.csv"

def load_cleaned(path):
    df = pd.read_csv(path, low_memory=False)

    # make invoice/order id consistent
    if "Invoice" in df.columns:
        df["Invoice"] = df["Invoice"].astype(str).str.strip()

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

def compute_kpis(df):
    total_revenue = df["Revenue"].sum()
    num_orders = df["Invoice"].nunique()
    unique_customers = df["Customer ID"].nunique()
    aov = total_revenue / num_orders if num_orders else 0

    return {
        "total_revenue": round(total_revenue, 2),
        "number_of_orders": int(num_orders),
        "unique_customers": int(unique_customers),
        "average_order_value": round(aov, 2)
    }

if __name__ == "__main__":
    df = load_cleaned(DATA_PATH)
    kpis = compute_kpis(df)

    print("=== CORE KPIs ===")
    for k, v in kpis.items():
        print(f"{k}: {v}")
