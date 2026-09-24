import pandas as pd

# load data
DATA_PATH = "data/raw/la_crime_2020_2024_raw.csv"

df = pd.read_csv(DATA_PATH)

# basic shape
print("\n=== DATASET SHAPE ===")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

# column names
print("\n=== COLUMNS ===")
for column in df.columns:
    print(column)

# data types
print("\n=== DATA TYPES ===")
print(df.dtypes)

# first five rows
print("\n=== FIRST FIVE ROWS ===")
print(df.head())

# missing vals
print("\n=== MISSING VALUES ===")
missing = df.isnull().sum().sort_values(ascending=False)

missing_pct = (df.isnull().mean() * 100).sort_values(ascending=False)

missing_summary = pd.DataFrame({
    "missing_count": missing,
    "missing_percent": missing_pct
})

print(missing_summary)

# unique values
print("\n=== UNIQUE VALUES ===")
for column in df.columns:
    print(f"{column}: {df[column].nunique(dropna=True):,}")

# duplicate rows
print("\n=== DUPLICATES ===")
print(f"Exact duplicate rows: {df.duplicated().sum():,}")
