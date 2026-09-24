# LA Crime Data Story

## Project Overview

This project explores crime records from Los Angeles from 2020 through 2024. The analysis focuses on the gap between the recorded date of occurrence and the recorded date of the crime report. The goal is to understand how common short occurrence-to-report gaps are, how often records have much longer gaps, and whether these patterns differ across crime types.

## Key Questions

- How long is the typical gap between the recorded occurrence date and report date?
- How common are long occurrence-to-report gaps?
- Does the pattern vary substantially across crime types?
- What limitations should be considered when interpreting these dates?

## Dataset

The project uses the City of Los Angeles dataset **Crime Data from 2020 to 2024**, published through the Los Angeles Open Data Portal and Data.gov. The dataset contains crime incidents recorded by the Los Angeles Police Department and covers incidents dating back to 2020. The dataset is historical. LAPD transitioned from its legacy Records Management System to a new NIBRS-aligned system in 2024, and the legacy dataset is no longer being updated.

Source:

City of Los Angeles, Crime Data from 2020 to 2024  
https://catalog.data.gov/dataset/crime-data-from-2020-to-present

## Data Limitations

The dataset documentation notes several limitations:

- Records were transcribed from original paper crime reports and may contain inaccuracies.
- The legacy dataset is no longer updated following LAPD's transition to its newer Records Management System.
- Location information is limited to the nearest hundred block for privacy.
- Some missing location fields are represented by 0° latitude and longitude.
- The report date and occurrence date should not automatically be interpreted as the amount of time a victim waited to report an incident.
- Differences across years may reflect differences in how long records have had to accumulate later report dates.

## Data Processing

The analysis follows a reproducible preprocessing and analysis pipeline.

### 01. Inspect Data

`scripts/01_inspect_data.py`

Examines:

- dataset dimensions
- column names
- data types
- missing values
- unique values
- duplicate records

### 02. Clean Data

`scripts/02_clean_data.py`

Performs basic data cleaning:

- converts date fields to datetime values
- identifies invalid dates
- checks for negative occurrence-to-report gaps
- identifies placeholder 0°/0° coordinates
- converts invalid victim ages to missing values
- removes exact duplicate rows
- creates the cleaned dataset

Output:

`data/cleaned/la_crime_2020_2024_clean.csv`

### 03. Explore Dates

`scripts/03_explore_dates.py`

Calculates overall occurrence-to-report delay statistics and examines the distribution of delays.

### 04. Delay by Year

`scripts/04_delay_by_year.py`

Examines reporting-delay patterns by occurrence year.

### 05. Delay by Crime

`scripts/05_delay_by_crime.py`

Compares reporting-delay statistics across crime types.

### 06. Visualize Delay

`scripts/06_visualize_delay.py`

Creates exploratory visualizations comparing reporting delays across crime types.

### 07. Delay Distribution

`scripts/07_delay_distribution.py`

Examines the overall distribution of reporting delays and the long right tail.

### 08. Feature Engineering

`scripts/08_feature_engineering.py`

Creates additional variables used in the analysis:

- reporting delay in days
- reporting delay category
- occurrence year
- occurrence month
- occurrence day of week
- occurrence hour

Output:

`data/cleaned/la_crime_2020_2024_engineered.csv`

### 09. Delay by Occurrence Time

`scripts/09_delay_by_occurrence_time.py`

Explores whether reporting-delay patterns vary by occurrence year, day of week, or hour.

### 10. Delay by Hour and Crime

`scripts/10_delay_by_hour_and_crime.py`

Investigates whether differences in reporting delay by occurrence hour may be related to differences in crime type.

### 11. Final Crime Type Analysis

`scripts/11_final_crime_type_analysis.py`

Creates the final crime-type summary using only crime categories with at least 2,000 records.

### 12. Final Visualizations

`scripts/12_final_visualizations.py`

Creates the final visualizations used to communicate the main findings.

## Main Findings

Across the full dataset:

- 47.97% of records have the same occurrence and report date.
- 38.88% have a gap of 1–7 days.
- 7.28% have a gap of 8–30 days.
- 5.12% have a gap of 31–365 days.
- 0.75% have a gap of more than one year.

The distribution therefore has a long tail. Most records have short occurrence-to-report gaps, but a smaller group has substantially longer gaps.

The pattern also varies substantially across crime types. Among crime categories with at least 2,000 records, embezzlement had a median occurrence-to-report gap of 34 days, with 53.52% of records having gaps greater than 30 days. In comparison, robbery had a median gap of 0 days and only 0.69% of records had gaps greater than 30 days.

## Reproducibility

### Requirements

Python 3.x

Install the required packages with:

```bash
pip install -r requirements.txt
```


### Running the Project

### Run the scripts in numerical order:

```python
python scripts/01_inspect_data.py
python scripts/02_clean_data.py
python scripts/03_explore_dates.py
python scripts/04_delay_by_year.py
python scripts/05_delay_by_crime.py
python scripts/06_visualize_delay.py
python scripts/07_delay_distribution.py
python scripts/08_feature_engineering.py
python scripts/09_delay_by_occurrence_time.py
python scripts/10_delay_by_hour_and_crime.py
python scripts/11_final_crime_type_analysis.py
python scripts/12_final_visualizations.py
```

## Project Structure
```
crime-data-story/
├── data/
│   ├── raw/
│   └── cleaned/
├── scripts/
├── outputs/
│   ├── figures/
│   └── tables/
├── presentation/
├── README.md
├── requirements.txt
└── .gitignore
```


## Ethical Considerations

Crime data describes real incidents and can affect how people perceive communities and victims. This project does not attempt to infer individual behavior or explain why a particular incident was reported when it was. The analysis describes patterns in the dates recorded in the dataset. Crime categories can also represent very different types of incidents, so comparisons should not be interpreted as measures of severity or importance. The analysis also avoids publishing precise addresses because the source dataset already limits addresses to the nearest hundred block for privacy.




###### Note from Ishan: AI Assistance AI tools were used to assist in the creation of this README.