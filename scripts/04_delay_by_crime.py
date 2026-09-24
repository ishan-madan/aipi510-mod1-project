import pandas as pd


# load data
DATA_PATH = "data/raw/la_crime_2020_2024_raw.csv"

df = pd.read_csv(DATA_PATH)


# convert dates
df["Date Rptd"] = pd.to_datetime(df["Date Rptd"])
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])


# calculate reporting delay
df["report_delay_days"] = (
    df["Date Rptd"] - df["DATE OCC"]
).dt.days


# calculate reporting delay metrics by crime type
crime_delay = (
    df.groupby("Crm Cd Desc")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        mean_delay="mean",
        same_day=lambda x: (x == 0).mean() * 100,
        over_30_days=lambda x: (x > 30).mean() * 100,
        over_365_days=lambda x: (x > 365).mean() * 100,
    )
)


# keep crime types with at least 500 incidents
crime_delay = crime_delay[
    crime_delay["count"] >= 500
]


# sort by percentage reported more than 30 days later
crime_delay = crime_delay.sort_values(
    "over_30_days",
    ascending=False
)


# display results
print("\n=== crime types with at least 500 incidents ===")
print(
    crime_delay.to_string(
        formatters={
            "median_delay": "{:.1f}".format,
            "mean_delay": "{:.1f}".format,
            "same_day": "{:.2f}%".format,
            "over_30_days": "{:.2f}%".format,
            "over_365_days": "{:.2f}%".format,
        }
    )
)


# top 15 crime types by percentage over 30 days
print("\n=== top 15 crime types by percentage reported over 30 days later ===")

print(
    crime_delay
    .head(15)
    .to_string(
        formatters={
            "median_delay": "{:.1f}".format,
            "mean_delay": "{:.1f}".format,
            "same_day": "{:.2f}%".format,
            "over_30_days": "{:.2f}%".format,
            "over_365_days": "{:.2f}%".format,
        }
    )
)


# top 15 crime types by median reporting delay
print("\n=== top 15 crime types by median reporting delay ===")

print(
    crime_delay
    .sort_values("median_delay", ascending=False)
    .head(15)
    .to_string(
        formatters={
            "median_delay": "{:.1f}".format,
            "mean_delay": "{:.1f}".format,
            "same_day": "{:.2f}%".format,
            "over_30_days": "{:.2f}%".format,
            "over_365_days": "{:.2f}%".format,
        }
    )
)