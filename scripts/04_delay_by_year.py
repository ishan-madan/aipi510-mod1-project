import pandas as pd


# load data
DATA_PATH = "data/clean/la_crime_2020_2024_clean.csv"

df = pd.read_csv(DATA_PATH)


# convert dates
df["Date Rptd"] = pd.to_datetime(df["Date Rptd"])
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])


# calculate reporting delay
df["report_delay_days"] = (
    df["Date Rptd"] - df["DATE OCC"]
).dt.days


# create occurrence year
df["occurrence_year"] = df["DATE OCC"].dt.year


# summary by occurrence year
print("\n=== reporting delay by occurrence year ===")

year_summary = (
    df.groupby("occurrence_year")["report_delay_days"]
    .agg(
        count="count",
        mean_delay="mean",
        median_delay="median",
        max_delay="max",
    )
)

year_summary["p75"] = (
    df.groupby("occurrence_year")["report_delay_days"]
    .quantile(0.75)
)

print(year_summary.to_string())


# percentage reported same day
print("\n=== same-day reporting by occurrence year ===")

same_day_by_year = (
    df.groupby("occurrence_year")["report_delay_days"]
    .apply(lambda x: (x == 0).mean() * 100)
)

print(same_day_by_year.to_string())


# percentage reported more than 30 days later
print("\n=== reports over 30 days later by occurrence year ===")

over_30_by_year = (
    df.groupby("occurrence_year")["report_delay_days"]
    .apply(lambda x: (x > 30).mean() * 100)
)

print(over_30_by_year.to_string())