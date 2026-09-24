import os
import pandas as pd

# load raw data
DATA_PATH = "data/clean/la_crime_2020_2024_clean.csv"

df = pd.read_csv(DATA_PATH)

print("\n=== original dataset ===")
print(f"rows: {len(df):,}")
print(f"columns: {len(df.columns)}")

# convert date columns
df["Date Rptd"] = pd.to_datetime(
    df["Date Rptd"],
    errors="coerce"
)

df["DATE OCC"] = pd.to_datetime(
    df["DATE OCC"],
    errors="coerce"
)

# convert time of occurrence to a four-digit string
df["TIME OCC"] = (
    df["TIME OCC"]
    .astype("Int64")
    .astype(str)
    .str.zfill(4)
)

# identify invalid date records
invalid_dates = (
    df["Date Rptd"].isna()
    | df["DATE OCC"].isna()
)

print("\n=== invalid dates ===")
print(f"records with invalid dates: {invalid_dates.sum():,}")

# identify records where the reported date occurs before the occurrence date
negative_delay = (
    df["Date Rptd"] < df["DATE OCC"]
)

print("\n=== negative reporting delays ===")
print(f"records with negative delays: {negative_delay.sum():,}")

# calculate reporting delay
df["report_delay_days"] = (
    df["Date Rptd"] - df["DATE OCC"]
).dt.days

# identify invalid geographic coordinates
invalid_coordinates = (
    (df["LAT"] == 0)
    & (df["LON"] == 0)
)

print("\n=== invalid geographic coordinates ===")
print(
    f"records with coordinates of 0,0: "
    f"{invalid_coordinates.sum():,}"
)

# replace 0,0 coordinates with missing values
df.loc[invalid_coordinates, ["LAT", "LON"]] = pd.NA

# check victim age values
invalid_age = (
    (df["Vict Age"] < 0)
    | (df["Vict Age"] > 120)
)

print("\n=== suspicious victim ages ===")
print(f"records with suspicious ages: {invalid_age.sum():,}")

# preserve unusual age values for review rather than deleting them
df.loc[invalid_age, "Vict Age"] = pd.NA

# remove exact duplicate records
duplicate_count = df.duplicated().sum()

print("\n=== duplicate records ===")
print(f"exact duplicate rows: {duplicate_count:,}")

df = df.drop_duplicates()

# remove records with invalid dates
df = df[
    df["Date Rptd"].notna()
    & df["DATE OCC"].notna()
].copy()

# recalculate reporting delay after cleaning
df["report_delay_days"] = (
    df["Date Rptd"] - df["DATE OCC"]
).dt.days

# remove records with negative reporting delays
df = df[
    df["report_delay_days"] >= 0
].copy()

# create cleaned data directory
os.makedirs("data/cleaned", exist_ok=True)

# save cleaned dataset
OUTPUT_PATH = "data/cleaned/la_crime_2020_2024_clean.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# print final dataset information
print("\n=== cleaned dataset ===")
print(f"rows: {len(df):,}")
print(f"columns: {len(df.columns)}")
print(f"saved to: {OUTPUT_PATH}")

# print remaining missing values
print("\n=== remaining missing values ===")

missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

print(
    missing[missing > 0].to_string()
)