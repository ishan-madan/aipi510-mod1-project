import pandas as pd

# load engineered data
DATA_PATH = (
    "data/cleaned/"
    "la_crime_2020_2024_engineered.csv"
)

df = pd.read_csv(DATA_PATH)

# calculate delay statistics by occurrence hour and crime type
hour_crime = (
    df.groupby(
        ["occurrence_hour", "Crm Cd Desc"]
    )["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        over_30_days=lambda x: (x > 30).mean() * 100,
    )
    .reset_index()
)

# keep crime types with at least 500 incidents overall
crime_counts = (
    df["Crm Cd Desc"]
    .value_counts()
)

valid_crimes = crime_counts[
    crime_counts >= 500
].index

hour_crime = hour_crime[
    hour_crime["Crm Cd Desc"].isin(valid_crimes)
]

# print overall hourly pattern
print("\n=== hourly reporting delay ===")

hour_summary = (
    df.groupby("occurrence_hour")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        over_30_days=lambda x: (x > 30).mean() * 100,
    )
)

print(
    hour_summary.round(2).to_string()
)

# identify the hours with the highest long-delay rates
print("\n=== hours with highest percentage over 30 days ===")

top_hours = (
    hour_summary
    .sort_values("over_30_days", ascending=False)
    .head(10)
)

print(
    top_hours.round(2).to_string()
)

# identify the hours with the lowest long-delay rates
print("\n=== hours with lowest percentage over 30 days ===")

bottom_hours = (
    hour_summary
    .sort_values("over_30_days")
    .head(10)
)

print(
    bottom_hours.round(2).to_string()
)

# compare crime composition at noon and midnight
print("\n=== top crime types at noon ===")

noon_crimes = (
    df[df["occurrence_hour"] == 12]["Crm Cd Desc"]
    .value_counts()
    .head(10)
)

print(noon_crimes.to_string())

print("\n=== top crime types at midnight ===")

midnight_crimes = (
    df[df["occurrence_hour"] == 0]["Crm Cd Desc"]
    .value_counts()
    .head(10)
)

print(midnight_crimes.to_string())

# compare crime composition at 6 pm and noon
print("\n=== top crime types at 6 pm ===")

evening_crimes = (
    df[df["occurrence_hour"] == 18]["Crm Cd Desc"]
    .value_counts()
    .head(10)
)

print(evening_crimes.to_string())

# identify crime types with the largest differences between
# their overall delay rate and their noon delay rate
print("\n=== noon delay rates for common crime types ===")

noon_delay = (
    df[df["occurrence_hour"] == 12]
    .groupby("Crm Cd Desc")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        over_30_days=lambda x: (x > 30).mean() * 100,
    )
)

noon_delay = noon_delay[
    noon_delay["count"] >= 100
]

print(
    noon_delay
    .sort_values("over_30_days", ascending=False)
    .head(20)
    .round(2)
    .to_string()
)