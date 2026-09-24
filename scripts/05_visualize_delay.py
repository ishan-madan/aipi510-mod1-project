import os
import pandas as pd
import matplotlib.pyplot as plt

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
        over_30_days=lambda x: (x > 30).mean() * 100,
    )
)

# keep crime types with at least 500 incidents
crime_delay = crime_delay[
    crime_delay["count"] >= 500
]

# create output directory
os.makedirs("outputs/figures", exist_ok=True)

# select top 15 crime types by percentage reported over 30 days
top_15 = (
    crime_delay
    .sort_values("over_30_days", ascending=False)
    .head(15)
    .sort_values("over_30_days")
)

# create chart for percentage reported over 30 days
plt.figure(figsize=(10, 8))

plt.barh(
    top_15.index,
    top_15["over_30_days"]
)

plt.xlabel("Percentage Reported More Than 30 Days Later")
plt.ylabel("Crime Type")
plt.title("Long Reporting Delays by Crime Type")

plt.tight_layout()

plt.savefig(
    "outputs/figures/reporting_delay_by_crime_type.png",
    dpi=300
)

plt.show()

# select top 15 crime types by median reporting delay
top_median = (
    crime_delay
    .sort_values("median_delay", ascending=False)
    .head(15)
    .sort_values("median_delay")
)

# create chart for median reporting delay
plt.figure(figsize=(10, 8))

plt.barh(
    top_median.index,
    top_median["median_delay"]
)

plt.xlabel("Median Reporting Delay (Days)")
plt.ylabel("Crime Type")
plt.title("Median Reporting Delay by Crime Type")

plt.tight_layout()

plt.savefig(
    "outputs/figures/median_reporting_delay_by_crime_type.png",
    dpi=300
)

plt.show()