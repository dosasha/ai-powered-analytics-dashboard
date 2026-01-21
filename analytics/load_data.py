import pandas as pd

# Path to raw dataset
DATA_PATH = "../data/raw/online_retail_II.csv"

def load_data(path):
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    df = load_data(DATA_PATH)

    print("Dataset Loaded Successfully\n")
    print("Shape of dataset:", df.shape)
    print("\nColumn names:")
    print(df.columns)

    print("\nMissing values per column:")
    print(df.isnull().sum())

    print("\nData types:")
    print(df.dtypes)

    print("\nFirst 5 rows:")
    print(df.head())
