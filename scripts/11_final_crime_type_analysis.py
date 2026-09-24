import pandas as pd

# load engineered data
DATA_PATH = (
    "data/cleaned/"
    "la_crime_2020_2024_engineered.csv"
)

df = pd.read_csv(DATA_PATH)

# calculate crime-level reporting delay statistics
crime_summary = (
    df.groupby("Crm Cd Desc")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        mean_delay="mean",
        over_30_days=lambda x: (x > 30).mean() * 100,
        over_365_days=lambda x: (x > 365).mean() * 100,
    )
)

# keep crime types with at least 2,000 incidents
crime_summary = crime_summary[
    crime_summary["count"] >= 2000
].copy()

# calculate percentage reported the same day
same_day = (
    df.groupby("Crm Cd Desc")["report_delay_days"]
    .apply(lambda x: (x == 0).mean() * 100)
)

crime_summary["same_day"] = same_day

# reorder columns
crime_summary = crime_summary[
    [
        "count",
        "median_delay",
        "mean_delay",
        "same_day",
        "over_30_days",
        "over_365_days",
    ]
]

# print number of crime types included
print("\n=== crime types with at least 2,000 incidents ===")
print(f"crime types included: {len(crime_summary)}")

# print crime types with the highest percentage over 30 days
print("\n=== highest percentage over 30 days ===")

top_30 = (
    crime_summary
    .sort_values("over_30_days", ascending=False)
    .head(20)
)

print(
    top_30.round(2).to_string()
)

# print crime types with the highest median delay
print("\n=== highest median reporting delay ===")

top_median = (
    crime_summary
    .sort_values("median_delay", ascending=False)
    .head(20)
)

print(
    top_median.round(2).to_string()
)

# print crime types with the highest percentage over one year
print("\n=== highest percentage over 365 days ===")

top_year = (
    crime_summary
    .sort_values("over_365_days", ascending=False)
    .head(20)
)

print(
    top_year.round(2).to_string()
)

# print the most common crime types for context
print("\n=== most common crime types ===")

most_common = (
    crime_summary
    .sort_values("count", ascending=False)
    .head(20)
)

print(
    most_common.round(2).to_string()
)

# save summary table
OUTPUT_PATH = (
    "outputs/tables/"
    "crime_type_reporting_delay_summary.csv"
)

import os

os.makedirs("outputs/tables", exist_ok=True)

crime_summary.sort_values(
    "over_30_days",
    ascending=False
).to_csv(OUTPUT_PATH)

print("\n=== output ===")
print(f"saved to: {OUTPUT_PATH}")