"""Prepare Pennsylvania ACS PUMS data; run from any working directory."""
from pathlib import Path
from zipfile import ZipFile
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
RAW_CSV = PROJECT_DIR / "psam_p42.csv"
RAW_ZIP = PROJECT_DIR / "csv_ppa.zip"
COLUMNS = ["SERIALNO", "AGEP", "SCHL", "ESR", "SEX", "RAC1P", "PWGTP"]

if RAW_CSV.exists():
    df = pd.read_csv(RAW_CSV, usecols=COLUMNS, dtype={"SERIALNO": str})
elif RAW_ZIP.exists():
    with ZipFile(RAW_ZIP) as archive:
        with archive.open("psam_p42.csv") as raw_file:
            df = pd.read_csv(raw_file, usecols=COLUMNS, dtype={"SERIALNO": str})
else:
    raise FileNotFoundError(
        "Place csv_ppa.zip or psam_p42.csv in the same folder as rawdata_clean.py."
    )

df["YEAR"] = df["SERIALNO"].str[:4].astype(int)
df = df.loc[df["AGEP"].between(25, 64)].copy()
df = df[["YEAR", "AGEP", "SCHL", "ESR", "SEX", "RAC1P", "PWGTP"]]
output_path = PROJECT_DIR / "pa_cleaned.csv"
df.to_csv(output_path, index=False)
print(f"Saved {len(df):,} rows to {output_path.name}")
