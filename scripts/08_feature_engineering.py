import os
import pandas as pd

# load cleaned data
DATA_PATH = "data/cleaned/la_crime_2020_2024_clean.csv"

df = pd.read_csv(DATA_PATH)

# convert date columns
df["Date Rptd"] = pd.to_datetime(df["Date Rptd"])
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])

# calculate reporting delay
df["report_delay_days"] = (
    df["Date Rptd"] - df["DATE OCC"]
).dt.days

# create reporting delay categories
df["delay_category"] = pd.cut(
    df["report_delay_days"],
    bins=[-1, 0, 7, 30, 365, float("inf")],
    labels=[
        "Same Day",
        "1–7 Days",
        "8–30 Days",
        "31–365 Days",
        "Over 365 Days",
    ]
)

# create occurrence year
df["occurrence_year"] = df["DATE OCC"].dt.year

# create occurrence month
df["occurrence_month"] = df["DATE OCC"].dt.month

# create day of week
df["occurrence_day_of_week"] = (
    df["DATE OCC"]
    .dt.day_name()
)

# convert time of occurrence to numeric
time_occ = pd.to_numeric(
    df["TIME OCC"],
    errors="coerce"
)

# extract occurrence hour
df["occurrence_hour"] = (
    time_occ // 100
).astype("Int64")

# validate occurrence hour
invalid_hours = (
    (df["occurrence_hour"] < 0)
    | (df["occurrence_hour"] > 23)
)

print("\n=== feature validation ===")
print(f"invalid occurrence hours: {invalid_hours.sum():,}")

# set invalid hours to missing
df.loc[
    invalid_hours,
    "occurrence_hour"
] = pd.NA

# print feature summaries
print("\n=== reporting delay categories ===")
print(
    df["delay_category"]
    .value_counts(dropna=False)
)

print("\n=== occurrence year ===")
print(
    df["occurrence_year"]
    .value_counts()
    .sort_index()
)

print("\n=== occurrence day of week ===")
print(
    df["occurrence_day_of_week"]
    .value_counts()
)

print("\n=== occurrence hour ===")
print(
    df["occurrence_hour"]
    .describe()
)

# create output directory
os.makedirs("data/cleaned", exist_ok=True)

# save engineered dataset
OUTPUT_PATH = (
    "data/cleaned/"
    "la_crime_2020_2024_engineered.csv"
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# print final dataset information
print("\n=== engineered dataset ===")
print(f"rows: {len(df):,}")
print(f"columns: {len(df.columns)}")
print(f"saved to: {OUTPUT_PATH}")

print("\n=== new features ===")

new_features = [
    "report_delay_days",
    "delay_category",
    "occurrence_year",
    "occurrence_month",
    "occurrence_day_of_week",
    "occurrence_hour",
]

for feature in new_features:
    print(f"- {feature}")