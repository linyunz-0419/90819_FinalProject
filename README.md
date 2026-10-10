# Educational Attainment and Unemployment in Pennsylvania, 2020–2024

## Project Overview

This statistical modeling project asks whether higher educational attainment is associated with lower unemployment among Pennsylvania adults aged 25–64 in the civilian labor force, after accounting for age, sex, race, and notebook-derived year labels.

The analysis combines survey-weighted descriptive statistics, visualizations, and weighted logistic regression. Findings describe associations rather than causal effects.

## Repository Contents

| File or Folder | Description |
|---|---|
| `csv_ppa.zip` | Original ACS PUMS Pennsylvania person-data archive |
| `rawdata_clean.py` | Cleaning script that reads the original CSV or ZIP and creates the prepared dataset |
| `pa_cleaned.csv` | Prepared dataset containing 322,000 records and seven variables |
| `Final_Project_Analysis.ipynb` | Feature construction, descriptive analysis, statistical modeling, and evaluation |
| `data_dictionary.md` | Project-specific variable definitions and recoding rules |
| `PUMS_Data_Dictionary_2020-2024.pdf` | Official Census source-variable dictionary |
| `requirements.txt` | Analysis dependencies and notebook runtime |
| `outputs/` | Generated figures and tables |
| `90813 Final Project Report.pdf` | Final research report |
| `README.md` | Project overview and reproduction instructions |

## Data Source

The project uses the U.S. Census Bureau's **2020–2024 American Community Survey (ACS) 5-Year Public Use Microdata Sample (PUMS), Pennsylvania person file**.

- Original archive: `csv_ppa.zip`, included in the repository.
- Person-level file inside the archive: `psam_p42.csv`.
- Official download: https://www2.census.gov/programs-surveys/acs/data/pums/2024/5-Year/csv_ppa.zip
- Documentation: https://www.census.gov/programs-surveys/acs/microdata/documentation/2024.html

The Census survey provides education, employment, demographic characteristics, and person weights suitable for this research question. The official dictionary documents source codes; the [project dictionary](data_dictionary.md) documents transformations used here.

## Sample and Feature Engineering

The cleaning script retains `AGEP`, `SCHL`, `ESR`, `SEX`, `RAC1P`, and `PWGTP`, derives `YEAR` from the first four characters of `SERIALNO`, and restricts age to 25–64. It produces 322,000 records.

The notebook then keeps the civilian labor force (`ESR` = 1, 2, or 3), yielding **249,839 respondents**, including **9,429 unemployed respondents**. Members of the Armed Forces and people outside the labor force are excluded.

The outcome is `UNEMPLOYED`: 1 for `ESR` = 3 and 0 for `ESR` = 1 or 2.

Education is grouped as follows:

| `SCHL` Code | `EDUCATION` Category |
|---|---|
| 1–15 | Less than High School |
| 16–17 | High School / GED |
| 18–20 | Some College / Associate |
| 21 | Bachelor's Degree |
| 22–24 | Graduate Degree |

Bachelor's degree is the model reference category. Education categories allow comparisons without assuming equal differences between qualification levels. Age, sex, race, and year labels adjust for observed demographic differences and variation across labels.

`RACE_GROUP` maps `RAC1P` = 1 to White, 2 to Black, 6 to Asian, and all remaining codes to Other / Multiracial. Source codes and additional constructed variables are detailed in `data_dictionary.md`.

## Analysis Methods

1. Calculate sample characteristics and unemployment rates using person weights (`PWGTP`).
2. Plot weighted unemployment by education and notebook-derived year label.
3. Fit a binomial generalized linear model with a logit link:

   ```python
   UNEMPLOYED ~ C(EDUCATION) + AGEP + C(SEX) + C(RACE_GROUP) + C(YEAR)
   ```

   `PWGTP` supplies frequency weights.
4. Report education odds ratios, confidence intervals, and survey-weighted averages of model-adjusted predicted unemployment probabilities.
5. Evaluate a separate model trained on 80% of observations, using a stratified 20% test split and `random_state=42`.

Evaluation uses a 0.5 classification threshold and reports unweighted test accuracy, precision, recall, ROC-AUC, and a confusion matrix. The full-sample model supplies the report's association estimates; the training-sample model supplies held-out evaluation.

## Main Findings

- Overall weighted unemployment is **4.45%**.
- Weighted unemployment declines from **8.15%** for less than high school to **1.94%** for graduate degree holders.
- Compared with bachelor's degree holders, adjusted unemployment odds ratios are **2.565** for less than high school, **1.958** for high school/GED, **1.585** for some college/associate, and **0.636** for graduate degree holders.
- Test accuracy is **96.2%**, but the classifier predicts everyone as employed at the 0.5 threshold. Unemployment precision and recall are both **0**, and ROC-AUC is **0.659**.

Higher education is associated with lower unemployment. The classifier has limited usefulness for identifying individual unemployed respondents, despite high accuracy.

## Reproducing the Analysis

These instructions apply to the accompanying corrected cleaning script and notebook. Place all project files at the repository root, using the filenames listed above.

### 1. Download the Repository

```bash
git clone https://github.com/linyunz-0419/90819_FinalProject.git
cd 90819_FinalProject
```

Alternatively, use **Code → Download ZIP**, extract the repository, and open a terminal in its folder.

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The analysis was checked using Python 3.12. Analysis package versions are pinned to the verification environment; the Jupyter notebook interface is listed separately without a version pin.

### 3. Generate the Prepared Data

Keep `csv_ppa.zip` in the same folder as `rawdata_clean.py`, then run:

```bash
python rawdata_clean.py
```

The script reads `psam_p42.csv` directly from the ZIP when no extracted CSV is present. If an extracted `psam_p42.csv` exists beside the script, it uses that file instead. The output is `pa_cleaned.csv` in the script's folder.

### 4. Run the Notebook

Start Jupyter from the repository root:

```bash
python -m notebook Final_Project_Analysis.ipynb
```

Restart the kernel and run all cells from top to bottom. The notebook reads `pa_cleaned.csv` from the working directory and creates `outputs/` if needed.

It generates:

| Output File | Content |
|---|---|
| `outputs/figure1_unemployment_by_education.png` | Weighted unemployment by education |
| `outputs/figure2_unemployment_by_education_year.png` | Weighted unemployment by education and year label |
| `outputs/figure3_predicted_probability_by_education.png` | Adjusted predicted unemployment probabilities |
| `outputs/table1_sample_characteristics.csv` | Sample characteristics |
| `outputs/table2_logistic_regression_results.csv` | Education odds ratios, confidence intervals, and p-values |

Evaluation metrics and the confusion matrix are displayed in the notebook.

### Verification

The corrected cleaning script reproduced the uploaded `pa_cleaned.csv` exactly. All notebook code cells were executed in order in a fresh Python process. Regenerated sample characteristics, education odds ratios, adjusted predictions, and evaluation metrics matched the report at the displayed precision.

## Limitations

- The analysis is observational and does not establish causality. Occupation and work experience are not fully controlled.
- `YEAR` is derived from `SERIALNO` in the pooled five-year data. The project has not independently validated these comparisons as separate annual estimates.
- Regression confidence intervals and p-values use default nonrobust covariance estimates and do not fully account for the ACS complex survey design.
- Unemployment is uncommon, and the reported threshold yields no positive unemployment predictions.

## Research Report

[Read the final research report](90813%20Final%20Project%20Report.pdf)
