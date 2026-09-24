import pandas as pd

# load engineered data
DATA_PATH = (
    "data/cleaned/la_crime_2020_2024_engineered.csv"
)

df = pd.read_csv(DATA_PATH)

# convert date columns
df["Date Rptd"] = pd.to_datetime(df["Date Rptd"])
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])

# make sure reporting delay is numeric
df["report_delay_days"] = pd.to_numeric(
    df["report_delay_days"],
    errors="coerce"
)

# analyze delay categories by occurrence year
print("\n=== delay categories by occurrence year ===")

year_delay = pd.crosstab(
    df["occurrence_year"],
    df["delay_category"],
    normalize="index"
) * 100

print(
    year_delay.round(2).to_string()
)

# analyze delay categories by day of week
print("\n=== delay categories by day of week ===")

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

day_delay = pd.crosstab(
    df["occurrence_day_of_week"],
    df["delay_category"],
    normalize="index"
) * 100

day_delay = day_delay.reindex(day_order)

print(
    day_delay.round(2).to_string()
)

# calculate median reporting delay by occurrence hour
print("\n=== reporting delay by occurrence hour ===")

hour_delay = (
    df.groupby("occurrence_hour")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        mean_delay="mean",
        over_30_days=lambda x: (x > 30).mean() * 100,
    )
)

print(
    hour_delay.round(2).to_string()
)

# calculate median reporting delay by day of week
print("\n=== reporting delay by day of week ===")

day_summary = (
    df.groupby("occurrence_day_of_week")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        mean_delay="mean",
        over_30_days=lambda x: (x > 30).mean() * 100,
    )
)

day_summary = day_summary.reindex(day_order)

print(
    day_summary.round(2).to_string()
)

# calculate overall delay category percentages
print("\n=== overall delay categories ===")

overall_delay = (
    df["delay_category"]
    .value_counts(normalize=True)
    * 100
)

print(
    overall_delay.round(2).to_string()
)