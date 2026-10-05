import pandas as pd

df = pd.read_csv("Final_Project/psam_p42.csv")

# keep variables needed for the project
df = df[
    ["AGEP", "SCHL", "ESR", "SEX", "RAC1P", "PWGTP"]
]

# working-age adults
df = df[
    (df["AGEP"] >= 25) &
    (df["AGEP"] <= 64)
]

df.to_csv("Final_Project/pa_cleaned.csv", index=False)