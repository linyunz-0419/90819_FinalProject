import pandas as pd

df = pd.read_csv("Final_Project/psam_p42.csv")

# keep variables needed for the project
df = df[
    ["SERIALNO", "AGEP", "SCHL", "ESR", "SEX", "RAC1P", "PWGTP"]
].copy()

# extract year from SERIALNO
df["YEAR"] = df["SERIALNO"].astype(str).str[:4].astype(int)

# working-age adults
df = df[
    (df["AGEP"] >= 25) &
    (df["AGEP"] <= 64)
]

# keep final variables
df = df[
    ["YEAR", "AGEP", "SCHL", "ESR", "SEX", "RAC1P", "PWGTP"]
]

df.to_csv("Final_Project/pa_cleaned.csv", index=False)