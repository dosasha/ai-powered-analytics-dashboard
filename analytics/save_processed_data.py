import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/online_retail_II.csv")
PROCESSED_PATH = Path("data/processed/online_retail_cleaned.csv")

df = pd.read_csv(RAW_PATH)

df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Revenue"] = df["Quantity"] * df["Price"]

PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(PROCESSED_PATH, index=False)

print("Processed dataset saved to:", PROCESSED_PATH)