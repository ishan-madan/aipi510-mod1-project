import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# load engineered data
DATA_PATH = (
    "data/cleaned/"
    "la_crime_2020_2024_engineered.csv"
)

df = pd.read_csv(DATA_PATH)

# create output directory
os.makedirs("outputs", exist_ok=True)

# calculate delay categories
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

# calculate crime-level statistics
crime_summary = (
    df.groupby("Crm Cd Desc")["report_delay_days"]
    .agg(
        count="count",
        median_delay="median",
        over_30_days=lambda x: (x > 30).mean() * 100,
        over_365_days=lambda x: (x > 365).mean() * 100,
    )
)

# use only crime types with at least 2,000 records
crime_summary = crime_summary[
    crime_summary["count"] >= 2000
].copy()

# top crime types by gaps over 30 days
top_30 = (
    crime_summary
    .sort_values("over_30_days", ascending=False)
    .head(7)
    .sort_values("over_30_days")
)


# top crime types by gaps over one year
top_365 = (
    crime_summary
    .sort_values("over_365_days", ascending=False)
    .head(5)
    .sort_values("over_365_days")
)

# color palette
NAVY = "#172033"
BLUE = "#356AE6"
BLUE_LIGHT = "#6F91E8"
TEAL = "#2A9D8F"
ORANGE = "#F4A261"
RED = "#E76F51"
LIGHT_BLUE = "#EEF3FF"
LIGHT_TEAL = "#EAF7F4"
LIGHT_RED = "#FFF0EC"
LIGHT_GRAY = "#F5F6F8"
MID_GRAY = "#697386"
DARK_GRAY = "#303846"
WHITE = "#FFFFFF"

# create figure
fig = plt.figure(
    figsize=(8.5, 11),
    facecolor=WHITE
)

# =========================================================
# TITLE
# =========================================================

fig.text(
    0.075,
    0.965,
    "When Is a Crime Reported?",
    fontsize=26,
    fontweight="bold",
    color=NAVY,
    va="top",
)

fig.text(
    0.075,
    0.932,
    "Exploring occurrence-to-report gaps in Los Angeles crime records, 2020–2024",
    fontsize=10.5,
    color=MID_GRAY,
    va="top",
)

fig.text(
    0.075,
    0.900,
    "1,004,894 CRIME RECORDS",
    fontsize=8,
    fontweight="bold",
    color=BLUE,
    va="top",
)

fig.add_artist(
    Rectangle(
        (0.075, 0.882),
        0.85,
        0.002,
        transform=fig.transFigure,
        facecolor="#DDE2EA",
        edgecolor="none",
    )
)

# =========================================================
# SECTION 1
# =========================================================

fig.text(
    0.075,
    0.850,
    "01  MOST RECORDS HAVE SHORT GAPS",
    fontsize=10,
    fontweight="bold",
    color=BLUE,
    va="top",
)

fig.text(
    0.075,
    0.810,
    "86.9%",
    fontsize=38,
    fontweight="bold",
    color=NAVY,
    va="top",
)

fig.text(
    0.075,
    0.765,
    "of records have an occurrence-to-report gap",
    fontsize=10.5,
    color=DARK_GRAY,
    va="top",
)

fig.text(
    0.075,
    0.740,
    "of 7 days or less",
    fontsize=12,
    fontweight="bold",
    color=DARK_GRAY,
    va="top",
)

# distribution bar
bar_ax = fig.add_axes(
    [0.075, 0.680, 0.85, 0.040]
)

bar_ax.set_xlim(0, 100)
bar_ax.set_ylim(0, 1)
bar_ax.axis("off")

bar_colors = [
    BLUE,
    BLUE_LIGHT,
    TEAL,
    ORANGE,
    RED,
]

left = 0

for percentage, color in zip(
    delay_percent,
    bar_colors
):
    bar_ax.barh(
        0,
        percentage,
        left=left,
        height=0.75,
        color=color,
    )
    left += percentage

# distribution labels
labels = [
    ("48.0%", "same day", BLUE),
    ("38.9%", "1–7 days", BLUE_LIGHT),
    ("7.3%", "8–30 days", TEAL),
    ("5.1%", "31–365 days", ORANGE),
    ("0.7%", "over 1 year", RED),
]

label_positions = [
    0.075,
    0.255,
    0.445,
    0.625,
    0.805,
]

for (value, label, color), x in zip(
    labels,
    label_positions
):
    fig.text(
        x,
        0.660,
        value,
        fontsize=10,
        fontweight="bold",
        color=color,
        va="top",
    )

    fig.text(
        x,
        0.642,
        label,
        fontsize=7.5,
        color=MID_GRAY,
        va="top",
    )

# =========================================================
# SECTION 2
# =========================================================

fig.text(
    0.075,
    0.600,
    "02  THE PATTERN CHANGES BY CRIME TYPE",
    fontsize=10,
    fontweight="bold",
    color=BLUE,
    va="top",
)

fig.text(
    0.075,
    0.570,
    "Crimes vs. Long Report Gaps",
    fontsize=12,
    fontweight="bold",
    color=NAVY,
    va="top",
)

# crime type chart
crime_ax = fig.add_axes(
    [0.175, 0.405, 0.8, 0.145]
)

crime_labels = [
    label.replace("EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)", "Embezzlement")
    .replace("DOCUMENT FORGERY / STOLEN FELONY", "Document forgery")
    .replace("THEFT OF IDENTITY", "Identity theft")
    .replace("LETTERS, LEWD  -  TELEPHONE CALLS, LEWD", "Lewd Calls")
    .replace("RAPE, FORCIBLE", "Rape")
    .replace("BUNCO, GRAND THEFT", "Grand Theft Bunco")
    .replace("BATTERY WITH SEXUAL CONTACT", "Battery w/ sexual contact")
    for label in top_30.index
]

crime_ax.barh(
    crime_labels,
    top_30["over_30_days"],
    color=BLUE,
    height=0.58,
)

crime_ax.set_xlim(
    0,
    top_30["over_30_days"].max() * 1.15
)

crime_ax.tick_params(
    axis="y",
    labelsize=7,
    colors=DARK_GRAY,
    length=0,
)

crime_ax.tick_params(
    axis="x",
    labelsize=6.5,
    colors=MID_GRAY,
    length=3,
)

crime_ax.set_xlabel(
    "% of records with gaps over 30 days",
    fontsize=6.8,
    color=MID_GRAY,
    labelpad=4,
)

crime_ax.spines["top"].set_visible(False)
crime_ax.spines["right"].set_visible(False)
crime_ax.spines["left"].set_visible(False)

crime_ax.grid(
    axis="x",
    alpha=0.15,
)

for i, value in enumerate(
    top_30["over_30_days"]
):
    crime_ax.text(
        value + 0.8,
        i,
        f"{value:.1f}%",
        va="center",
        fontsize=7,
        fontweight="bold",
        color=NAVY,
    )

# =========================================================
# CALLOUT CARDS
# =========================================================

# card 1
card1 = fig.add_axes(
    [0.075, 0.315, 0.405, 0.050]
)

card1.set_facecolor(LIGHT_BLUE)
card1.axis("off")

card1.text(
    0.06,
    0.62,
    "53.5%",
    fontsize=15,
    fontweight="bold",
    color=BLUE,
    va="center",
)

card1.text(
    0.29,
    0.62,
    "Embezzlement",
    fontsize=8.5,
    fontweight="bold",
    color=NAVY,
    va="center",
)

card1.text(
    0.29,
    0.25,
    "had gaps over 30 days",
    fontsize=7,
    color=MID_GRAY,
    va="center",
)

# card 2
card2 = fig.add_axes(
    [0.515, 0.315, 0.405, 0.050]
)

card2.set_facecolor(LIGHT_TEAL)
card2.axis("off")

card2.text(
    0.06,
    0.62,
    "0.7%",
    fontsize=15,
    fontweight="bold",
    color=TEAL,
    va="center",
)

card2.text(
    0.29,
    0.62,
    "Robbery",
    fontsize=8.5,
    fontweight="bold",
    color=NAVY,
    va="center",
)

card2.text(
    0.29,
    0.25,
    "had gaps over 30 days",
    fontsize=7,
    color=MID_GRAY,
    va="center",
)

# =========================================================
# SECTION 3
# =========================================================

fig.text(
    0.075,
    0.290,
    "03  THE LONG TAIL EXTENDS BEYOND A YEAR",
    fontsize=10,
    fontweight="bold",
    color=RED,
    va="top",
)

# large stat on left
fig.text(
    0.075,
    0.250,
    "0.75%",
    fontsize=27,
    fontweight="bold",
    color=NAVY,
    va="top",
)

fig.text(
    0.075,
    0.215,
    "of all records have gaps",
    fontsize=9.5,
    color=DARK_GRAY,
    va="top",
)

fig.text(
    0.075,
    0.192,
    "of more than one year.",
    fontsize=9.5,
    fontweight="bold",
    color=DARK_GRAY,
    va="top",
)

# long-tail chart on right
long_ax = fig.add_axes(
    [0.465, 0.105, 0.485, 0.145]
)

long_labels = [
    label.replace("RAPE, FORCIBLE", "Rape")
    .replace("THEFT OF IDENTITY", "Identity theft")
    .replace("LETTERS, LEWD  -  TELEPHONE CALLS, LEWD", "Lewd Letters/Calls")
    .replace("BATTERY WITH SEXUAL CONTACT", "Battery w/ sexual contact")
    .replace("DOCUMENT FORGERY / STOLEN FELONY", "Document forgery")
    .replace("EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)", "Embezzlement")
    for label in top_365.index
]

long_ax.barh(
    long_labels,
    top_365["over_365_days"],
    color=RED,
    height=0.55,
)

long_ax.set_xlim(
    0,
    top_365["over_365_days"].max() * 1.18
)

long_ax.tick_params(
    axis="y",
    labelsize=6.5,
    colors=DARK_GRAY,
    length=0,
)

long_ax.tick_params(
    axis="x",
    labelsize=6,
    colors=MID_GRAY,
)

long_ax.set_xlabel(
    "% with gaps over 1 year",
    fontsize=6.5,
    color=MID_GRAY,
    labelpad=3,
)

long_ax.spines["top"].set_visible(False)
long_ax.spines["right"].set_visible(False)
long_ax.spines["left"].set_visible(False)

long_ax.grid(
    axis="x",
    alpha=0.15,
)

for i, value in enumerate(
    top_365["over_365_days"]
):
    long_ax.text(
        value + 0.08,
        i,
        f"{value:.1f}%",
        va="center",
        fontsize=6.5,
        fontweight="bold",
        color=NAVY,
    )

# =========================================================
# TAKEAWAY
# =========================================================

takeaway = fig.add_axes(
    [0.05, 0.075, 0.335, 0.105]
)

takeaway.set_facecolor(LIGHT_RED)
takeaway.axis("off")

takeaway.text(
    0.07,
    0.82,
    "THE TAKEAWAY",
    fontsize=7.5,
    fontweight="bold",
    color=RED,
    va="center",
)

takeaway.text(
    0.07,
    0.58,
    "Most records have short",
    fontsize=9,
    fontweight="bold",
    color=NAVY,
    va="center",
)

takeaway.text(
    0.07,
    0.36,
    "gaps, but the long tail varies",
    fontsize=9,
    fontweight="bold",
    color=NAVY,
    va="center",
)

takeaway.text(
    0.07,
    0.14,
    "sharply across crime types.",
    fontsize=9,
    fontweight="bold",
    color=NAVY,
    va="center",
)


# =========================================================
# SOURCE
# =========================================================

fig.text(
    0.075,
    0.030,
    "Source: City of Los Angeles, Crime Data from 2020 to 2024",
    fontsize=6.5,
    color=MID_GRAY,
    va="bottom",
)

# save
png_path = "outputs/la_crime_data_infographic.png"
pdf_path = "outputs/la_crime_data_infographic.pdf"

plt.savefig(
    png_path,
    dpi=300,
    facecolor=WHITE,
)

plt.savefig(
    pdf_path,
    dpi=300,
    facecolor=WHITE,
)

plt.close()

print("\n=== infographic created ===")
print(f"png: {png_path}")
print(f"pdf: {pdf_path}")