# Project Data Dictionary

## Scope

`pa_cleaned.csv` contains seven columns and 322,000 adults aged 25–64. It is an input dataset: the notebook applies the civilian labor-force restriction and constructs analytical features in memory. The final analytic sample has 249,839 records.

No missing values were found in any of the seven columns in the supplied cleaned data. The cleaning script does not apply a separate missing-value imputation or deletion rule. The notebook selects `ESR` codes 1, 2, and 3. All selected respondents received an education category in the supplied data.

For full source coding, see `PUMS_Data_Dictionary_2020-2024.pdf`.

## Cleaned Dataset Columns

| Column | Meaning | Coding / Unit | Role |
|---|---|---|---|
| `YEAR` | Notebook-derived year label | Integer; first four characters of raw `SERIALNO`, 2020–2024 | Categorical model control and grouped comparisons; not independently validated annual estimates |
| `AGEP` | Age | Years; retained range 25–64 inclusive | Continuous model control |
| `SCHL` | Highest educational attainment | Census integer codes; grouping below | Source for `EDUCATION` |
| `ESR` | Employment status recode | 1 = civilian employed at work; 2 = civilian employed with a job but not at work; 3 = unemployed; 4–5 = Armed Forces; 6 = not in labor force | Select codes 1–3 for the analytic sample |
| `SEX` | Sex | 1 = male; 2 = female | Categorical control; male reference in this model |
| `RAC1P` | Census recoded race | Source codes documented in the official dictionary | Source for `RACE_GROUP` |
| `PWGTP` | Person weight | Person-level survey weight | Weighted descriptive estimates, frequency-weighted GLM, and weighted averages of adjusted predictions |

`SERIALNO` is read from the raw file to derive `YEAR`, then excluded from `pa_cleaned.csv`.

## Notebook Features

| Feature | Definition / Unit |
|---|---|
| `UNEMPLOYED` | 1 if `ESR` = 3; 0 if `ESR` = 1 or 2, within the analytic sample |
| `EDUCATION` | Five qualification groups derived from `SCHL`; see mapping below |
| `RACE_GROUP` | White, Black, Asian, or Other / Multiracial; see mapping below |
| `WEIGHTED_UNEMPLOYED` | `UNEMPLOYED * PWGTP`; weighted contribution to unemployed population estimates |
| `UNEMPLOYMENT_RATE` | In `trend_df`, 100 × sum of `WEIGHTED_UNEMPLOYED` / sum of `PWGTP`, within each year-label/education group; percentage |
| `PREDICTED_PROBABILITY` | Model probability of unemployment; fraction between 0 and 1 |
| `PREDICTED_CLASS` | In `test_df`, 1 if predicted probability ≥ 0.5; otherwise 0 |
| `Predicted Unemployment Probability (%)` | In `predicted_df`, 100 × PWGTP-weighted mean prediction after setting all respondents to one education category while retaining other covariates |

## Education Mapping

| `SCHL` Codes | `EDUCATION` Label |
|---|---|
| 1–15 | Less than High School |
| 16–17 | High School / GED |
| 18–20 | Some College / Associate |
| 21 | Bachelor's Degree |
| 22–24 | Graduate Degree |

The notebook implements the first group as `SCHL <= 15`, returns `None` for values outside its rules, and does not separately impute unknown education. The supplied analytic sample has no unassigned education values.

## Race Mapping

| `RAC1P` | `RACE_GROUP` |
|---|---|
| 1 | White |
| 2 | Black |
| 6 | Asian |
| All remaining codes | Other / Multiracial |

The implementation uses an `else` branch for the final category. No missing `RAC1P` values occur in the supplied cleaned data.

## Model Coding and Evaluation

The formula is:

```python
UNEMPLOYED ~ C(EDUCATION) + AGEP + C(SEX) + C(RACE_GROUP) + C(YEAR)
```

The formula interface constructs categorical indicators and includes an intercept. With the current string/integer categories, the reference groups are Bachelor's Degree, SEX = 1, Asian, and YEAR = 2020. Age enters as a continuous linear term on the log-odds scale.

Both fitted models use `PWGTP` as frequency weights. The report's odds ratios and adjusted predictions come from the full-sample model. Evaluation uses a separate model fitted to an 80% training sample; `train_test_split` uses `test_size=0.2`, `random_state=42`, and stratification by `UNEMPLOYED`.

Test metrics are unweighted because the metric calls do not pass `sample_weight`. The test sample contains 49,968 records. Classification uses a threshold of 0.5; ROC-AUC uses continuous predicted probabilities.
