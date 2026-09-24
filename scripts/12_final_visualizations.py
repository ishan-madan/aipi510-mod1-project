import os
import pandas as pd
import matplotlib.pyplot as plt

# load engineered data
DATA_PATH = (
    "data/cleaned/"
    "la_crime_2020_2024_engineered.csv"
)

df = pd.read_csv(DATA_PATH)

# create output directory
os.makedirs("outputs/figures", exist_ok=True)

# ============================================================
# overall reporting delay
# ============================================================

delay_order = [
    "Same Day",
    "1–7 Days",
    "8–30 Days",
    "31–365 Days",
    "Over 365 Days",
]

delay_counts = (
    df["delay_category"]
    .value_counts()
    .reindex(delay_order)
)

delay_percent = (
    delay_counts / len(df) * 100
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    delay_percent.index,
    delay_percent.values
)

plt.xlabel("Gap Between Occurrence Date and Report Date")
plt.ylabel("Percentage of Incidents")
plt.title(
    "Most LA Crime Records Have Short Occurrence-to-Report Gaps"
)

plt.ylim(0, max(delay_percent.values) * 1.15)

for bar, value in zip(bars, delay_percent.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        f"{value:.1f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "outputs/figures/final_overall_delay_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# crime type comparison
# ============================================================

crime_summary = (
    df.groupby("Crm Cd Desc")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        over_30_days=lambda x: (x > 30).mean() * 100,
        over_365_days=lambda x: (x > 365).mean() * 100,
    )
)

# keep crime types with at least 2,000 incidents
crime_summary = crime_summary[
    crime_summary["count"] >= 2000
]

# select the crime types with the highest percentage
# of records reported more than 30 days later
top_crimes = (
    crime_summary
    .sort_values("over_30_days", ascending=False)
    .head(12)
    .sort_values("over_30_days")
)

plt.figure(figsize=(11, 8))

bars = plt.barh(
    top_crimes.index,
    top_crimes["over_30_days"]
)

plt.xlabel(
    "Percentage of Records More Than 30 Days After Occurrence"
)
plt.ylabel("Crime Type")
plt.title(
    "Long Occurrence-to-Report Gaps Vary Sharply by Crime Type"
)

for bar, value in zip(
    bars,
    top_crimes["over_30_days"]
):
    plt.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}%",
        va="center"
    )

plt.xlim(
    0,
    top_crimes["over_30_days"].max() * 1.15
)

plt.tight_layout()

plt.savefig(
    "outputs/figures/final_delay_by_crime_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# very long reporting delays
# ============================================================

top_long_delay = (
    crime_summary
    .sort_values("over_365_days", ascending=False)
    .head(10)
    .sort_values("over_365_days")
)

plt.figure(figsize=(11, 7))

bars = plt.barh(
    top_long_delay.index,
    top_long_delay["over_365_days"]
)

plt.xlabel(
    "Percentage of Records More Than 365 Days After Occurrence"
)
plt.ylabel("Crime Type")
plt.title(
    "A Small Share of Records Have Gaps of More Than One Year"
)

for bar, value in zip(
    bars,
    top_long_delay["over_365_days"]
):
    plt.text(
        bar.get_width() + 0.05,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}%",
        va="center"
    )

plt.xlim(
    0,
    top_long_delay["over_365_days"].max() * 1.18
)

plt.tight_layout()

plt.savefig(
    "outputs/figures/final_long_delay_by_crime_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# print final statistics
# ============================================================

print("\n=== final visualization statistics ===")

print("\nOverall delay distribution:")

for category in delay_order:
    print(
        f"{category}: "
        f"{delay_percent[category]:.2f}%"
    )

print("\nTop crime types by percentage over 30 days:")

print(
    top_crimes[
        ["count", "median_delay", "over_30_days"]
    ]
    .sort_values(
        "over_30_days",
        ascending=False
    )
    .round(2)
    .to_string()
)

print("\nTop crime types by percentage over 365 days:")

print(
    top_long_delay[
        ["count", "median_delay", "over_365_days"]
    ]
    .sort_values(
        "over_365_days",
        ascending=False
    )
    .round(2)
    .to_string()
)

print("\n=== saved figures ===")
print(
    "outputs/figures/final_overall_delay_distribution.png"
)
print(
    "outputs/figures/final_delay_by_crime_type.png"
)
print(
    "outputs/figures/final_long_delay_by_crime_type.png"
)