import pandas as pd


# load data
DATA_PATH = "data/clean/la_crime_2020_2024_clean.csv"

df = pd.read_csv(DATA_PATH)


# convert dates
df["Date Rptd"] = pd.to_datetime(df["Date Rptd"])
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])


# calculate reporting delay in days
df["report_delay_days"] = (
    df["Date Rptd"] - df["DATE OCC"]
).dt.days


# basic statistics
print("\n=== REPORTING DELAY STATISTICS ===")
print(df["report_delay_days"].describe())


# negative reporting delays
print("\n=== NEGATIVE REPORTING DELAYS ===")
negative_delays = (df["report_delay_days"] < 0).sum()
print(f"Negative delays: {negative_delays:,}")


# same-day reports
print("\n=== SAME-DAY REPORTS ===")
same_day = (df["report_delay_days"] == 0).mean() * 100
print(f"Same-day reports: {same_day:.2f}%")


# 1 day reports
print("\n=== REPORTS WITHIN 1 DAY ===")
within_1_day = (df["report_delay_days"] <= 1).mean() * 100
print(f"Within 1 day: {within_1_day:.2f}%")


# 7 day reports
print("\n=== REPORTS WITHIN 7 DAYS ===")
within_7_days = (df["report_delay_days"] <= 7).mean() * 100
print(f"Within 7 days: {within_7_days:.2f}%")


# 30+ day reports
print("\n=== REPORTS MORE THAN 30 DAYS LATER ===")
over_30_days = (df["report_delay_days"] > 30).mean() * 100
print(f"More than 30 days: {over_30_days:.2f}%")


# 1+ year reports
print("\n=== REPORTS MORE THAN 1 YEAR LATER ===")
over_1_year = (df["report_delay_days"] > 365).mean() * 100
print(f"More than 1 year: {over_1_year:.2f}%")


# longest reporting delays
print("\n=== LONGEST REPORTING DELAYS ===")

longest_delays = (
    df[
        [
            "DR_NO",
            "Date Rptd",
            "DATE OCC",
            "report_delay_days",
            "Crm Cd Desc",
            "AREA NAME",
        ]
    ]
    .sort_values("report_delay_days", ascending=False)
    .head(10)
)

print(longest_delays.to_string(index=False))


# reporting delay by crime type
print("\n=== REPORTING DELAY BY CRIME TYPE ===")

crime_delay = (
    df.groupby("Crm Cd Desc")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        mean_delay="mean",
    )
    .sort_values("median_delay", ascending=False)
)

print(crime_delay.head(20).to_string())


# crime types with longest average delays
print("\n=== LONGEST AVERAGE DELAYS BY CRIME TYPE ===")
print(
    crime_delay
    .sort_values("mean_delay", ascending=False)
    .head(20)
    .to_string()
)