import os
import pandas as pd
import matplotlib.pyplot as plt

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

# print overall distribution statistics
print("\n=== reporting delay distribution ===")
print(df["report_delay_days"].describe())

# print selected percentiles
print("\n=== reporting delay percentiles ===")

percentiles = df["report_delay_days"].quantile(
    [0.50, 0.75, 0.90, 0.95, 0.99]
)

print(percentiles)

# calculate percentage reported within selected time periods
print("\n=== reporting delay ranges ===")

same_day = (df["report_delay_days"] == 0).mean() * 100
within_1_day = (df["report_delay_days"] <= 1).mean() * 100
within_7_days = (df["report_delay_days"] <= 7).mean() * 100
within_30_days = (df["report_delay_days"] <= 30).mean() * 100
over_30_days = (df["report_delay_days"] > 30).mean() * 100
over_365_days = (df["report_delay_days"] > 365).mean() * 100

print(f"same day: {same_day:.2f}%")
print(f"within 1 day: {within_1_day:.2f}%")
print(f"within 7 days: {within_7_days:.2f}%")
print(f"within 30 days: {within_30_days:.2f}%")
print(f"more than 30 days: {over_30_days:.2f}%")
print(f"more than 365 days: {over_365_days:.2f}%")

# create output directory
os.makedirs("outputs/figures", exist_ok=True)

# create histogram for delays up to 30 days
delay_under_30 = df[
    df["report_delay_days"] <= 30
]

plt.figure(figsize=(10, 6))

plt.hist(
    delay_under_30["report_delay_days"],
    bins=31,
    edgecolor="black"
)

plt.xlabel("Reporting Delay (Days)")
plt.ylabel("Number of Incidents")
plt.title("Incidents Reported Within 30 Days")

plt.tight_layout()

plt.savefig(
    "outputs/figures/reporting_delay_distribution_30_days.png",
    dpi=300
)

plt.show()

# create histogram to show the long tail
positive_delays = df[
    df["report_delay_days"] > 0
]

plt.figure(figsize=(10, 6))

plt.hist(
    positive_delays["report_delay_days"],
    bins=50,
    edgecolor="black"
)

plt.xscale("log")

plt.xlabel("Reporting Delay (Days, Log Scale)")
plt.ylabel("Number of Incidents")
plt.title("Incidents Reported With Long Delays (Log Scale)")

plt.tight_layout()

plt.savefig(
    "outputs/figures/reporting_delay_distribution_log.png",
    dpi=300
)

plt.show()