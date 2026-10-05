# Python Final Project

## Data Source

This project uses data from the U.S. Census Bureau's **2020–2024 American Community Survey (ACS) 5-Year Public Use Microdata Sample (PUMS)**.

The analysis uses the **Pennsylvania Person File**.

### Raw Data

The original data were downloaded from the official U.S. Census Bureau ACS PUMS FTP directory:

https://www2.census.gov/programs-surveys/acs/data/pums/2024/5-Year/

The original ZIP file used in this project is:

`csv_ppa.zip`

Direct download link:

https://www2.census.gov/programs-surveys/acs/data/pums/2024/5-Year/csv_ppa.zip

After extraction, the Pennsylvania person-level dataset is:

`psam_p42.csv`

Because the original raw CSV file is large, it is not stored directly in this GitHub repository. The raw data can be downloaded from the official Census Bureau link above. The cleaning script included in this repository can then be used to reproduce the cleaned dataset used in the analysis.

---

## Cleaned Data

The cleaned dataset used for analysis is:

`pa_cleaned.csv`

The cleaning process keeps the variables needed for this project and restricts the sample to working-age adults aged 25 to 64.

The cleaned dataset can be reproduced from the original Census PUMS data using:

`rawdata_clean.py`

---

## Variables

The main variables used in this project are listed below.

| Variable | Description | Use in This Project |
|----------|-------------|---------------------|
| `YEAR` | Data year | Identifies whether the observation comes from 2020, 2021, 2022, 2023, or 2024; extracted from the first four digits of `SERIALNO` |
| `AGEP` | Age | Used to restrict the sample to adults aged 25–64 and as a control variable |
| `SCHL` | Educational attainment | Main explanatory variable measuring level of education |
| `ESR` | Employment status recode | Used to identify labor-force status and unemployment |
| `SEX` | Sex | Used as a demographic control variable |
| `RAC1P` | Recoded detailed race code | Used as a demographic control or descriptive variable |
| `PWGTP` | Person's weight | Used to produce population-representative weighted estimates |
### Variable Details

#### YEAR — Data Year

`YEAR` identifies the year associated with each observation in the 2020–2024 ACS 5-Year PUMS dataset.

The variable is created from the first four digits of `SERIALNO`. It takes values from **2020 to 2024**.

In this project, `YEAR` is used to distinguish observations across years and can be used to examine changes in unemployment over time.

#### AGEP — Age

`AGEP` records the person's age in years.

In this project, the sample is restricted to individuals between **25 and 64 years old**.

#### SCHL — Educational Attainment

`SCHL` records the highest level of educational attainment completed by the respondent.

This is the main explanatory variable in the analysis. It is used to examine the relationship between educational attainment and unemployment.

#### ESR — Employment Status Recode

`ESR` identifies a person's employment and labor-force status.

It distinguishes individuals who are employed, unemployed, or not in the labor force.

In this project, `ESR` is used to identify the labor-force population and construct the unemployment outcome.

#### SEX — Sex

`SEX` identifies the respondent's sex.

It is used as a demographic control variable in the analysis.

#### RAC1P — Recoded Detailed Race Code

`RAC1P` identifies the respondent's race using Census Bureau race categories.

The major codes are:

- `1` = White alone
- `2` = Black or African American alone
- `3` = American Indian alone
- `4` = Alaska Native alone
- `5` = American Indian or Alaska Native categories
- `6` = Asian alone
- `7` = Native Hawaiian and Other Pacific Islander alone
- `8` = Some Other Race alone
- `9` = Two or More Races

#### PWGTP — Person's Weight

`PWGTP` is the person-level survey weight provided by the Census Bureau.

Each PUMS observation represents more than one person in the population. `PWGTP` is therefore used to calculate weighted statistics so that estimates better represent the Pennsylvania population.

---

## Official Data Dictionary

Variable definitions and coding information come from the U.S. Census Bureau's official ACS PUMS documentation.

2024 PUMS documentation page:

https://www.census.gov/programs-surveys/acs/microdata/documentation/2024.html

2020–2024 ACS 5-Year PUMS Data Dictionary:

https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2020-2024.pdf

The Census Bureau data dictionary provides the official definitions and coding schemes for variables including `AGEP`, `SCHL`, `ESR`, `SEX`, `RAC1P`, and `PWGTP`.

---

## Reproducibility

The analysis can be reproduced using the following steps:

1. Download `csv_ppa.zip` from the U.S. Census Bureau.
2. Extract the ZIP file.
3. Place the extracted Pennsylvania person file in the project directory.
4. Run `rawdata_clean.py` to generate `pa_cleaned.csv`.
5. Run the analysis code using the cleaned dataset.

All data cleaning and analysis code used in the project is included in this repository.
