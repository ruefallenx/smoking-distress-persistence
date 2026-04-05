import pandas as pd
import pyreadstat
import numpy as np
import statsmodels.formula.api as smf

# =================================================
# FILE PATHS
# =================================================
wave7_file = r"G:\Github\data\DS7001\36498-7001-Data.dta"
wave6_file = r"G:\Github\data\DS6001\36498-6001-Data.dta"

# =================================================
# LOAD ONLY NEEDED COLUMNS
# =================================================
usecols_w6 = [
    "PERSONID",
    "R06_AX0091",
    "R06_AC1003",
    "R06R_A_AGECAT6",
    "R06R_A_SEX",
    "R06R_A_AM0018_V2",
    "R06R_A_AM0030"
]

usecols_w7 = [
    "PERSONID",
    "R07_AX0091",
    "R07_AC1003"
]

print("Loading Wave 6...")
w6, meta6 = pyreadstat.read_dta(
    wave6_file,
    usecols=usecols_w6,
    apply_value_formats=False
)

print("Loading Wave 7...")
w7, meta7 = pyreadstat.read_dta(
    wave7_file,
    usecols=usecols_w7,
    apply_value_formats=False
)

# =================================================
# RENAME
# =================================================
w6 = w6.rename(columns={
    "R06_AX0091": "mh_w6",
    "R06_AC1003": "smoke_w6",
    "R06R_A_AGECAT6": "agecat_w6",
    "R06R_A_SEX": "sex_w6",
    "R06R_A_AM0018_V2": "edu_w6",
    "R06R_A_AM0030": "income_w6"
})

w7 = w7.rename(columns={
    "R07_AX0091": "mh_w7",
    "R07_AC1003": "smoke_w7"
})

# =================================================
# MERGE
# =================================================
df = pd.merge(w6, w7, on="PERSONID", how="inner")
print("Merged shape:", df.shape)

# =================================================
# CLEAN MH
# =================================================
df = df[df["mh_w6"].isin([1, 2, 3, 4, 5])]
df = df[df["mh_w7"].isin([1, 2, 3, 4, 5])]

# =================================================
# CLEAN SMOKING
# =================================================
df = df[df["smoke_w6"].isin([-1, 1, 2, 3])]
df = df[df["smoke_w7"].isin([-1, 1, 2, 3])]

# =================================================
# CLEAN DEMOGRAPHICS
# =================================================
for col in ["agecat_w6", "sex_w6", "edu_w6", "income_w6"]:
    df = df[pd.to_numeric(df[col], errors="coerce").notna()]
    df = df[df[col] >= 0]

print("Shape after cleaning demographics:", df.shape)

print("\nagecat_w6")
print(df["agecat_w6"].value_counts(dropna=False).sort_index())

# =================================================
# PRIMARY DISTRESS DEFINITION
# =================================================
df["high_w6"] = df["mh_w6"].isin([4, 5])
df["high_w7"] = df["mh_w7"].isin([4, 5])

def classify_pattern(high_w6, high_w7):
    if high_w6 and high_w7:
        return "persistent"
    elif high_w6 and not high_w7:
        return "transient_w6_only"
    elif not high_w6 and high_w7:
        return "emergent_w7_only"
    else:
        return "low_low"

df["pattern"] = df.apply(
    lambda row: classify_pattern(row["high_w6"], row["high_w7"]),
    axis=1
)

# =================================================
# RECODE SMOKING
# =================================================
df["smoker_w6"] = df["smoke_w6"].isin([1, 2]).astype(int)
df["smoker_w7"] = df["smoke_w7"].isin([1, 2]).astype(int)

df["pattern"] = pd.Categorical(
    df["pattern"],
    categories=["low_low", "transient_w6_only", "emergent_w7_only", "persistent"]
)

for col in ["agecat_w6", "sex_w6", "edu_w6", "income_w6"]:
    df[col] = df[col].astype("category")

# =================================================
# MODEL 1
# =================================================
m1 = smf.logit(
    "smoker_w7 ~ C(pattern, Treatment(reference='low_low')) + smoker_w6",
    data=df
).fit()

# =================================================
# MODEL 2
# =================================================
m2 = smf.logit(
    "smoker_w7 ~ C(pattern, Treatment(reference='low_low')) + smoker_w6 + C(agecat_w6) + C(sex_w6) + C(edu_w6) + C(income_w6)",
    data=df
).fit()

def extract_or_table(model, label):
    params = model.params
    conf = model.conf_int()
    out = pd.DataFrame({
        "OR": np.exp(params),
        "CI_low": np.exp(conf[0]),
        "CI_high": np.exp(conf[1]),
        "p_value": model.pvalues
    })
    out["model"] = label
    return out

or1 = extract_or_table(m1, "baseline_only")
or2 = extract_or_table(m2, "demographic_adjusted_agecat")

print("\n=== BASELINE-ONLY MODEL ===")
print(or1)

print("\n=== DEMOGRAPHIC-ADJUSTED MODEL (AGECAT) ===")
print(or2)

cmp1 = or1[or1.index.str.contains("pattern", regex=False)].copy()
cmp2 = or2[or2.index.str.contains("pattern", regex=False)].copy()

cmp1 = cmp1[["OR", "CI_low", "CI_high", "p_value"]]
cmp2 = cmp2[["OR", "CI_low", "CI_high", "p_value"]]

cmp1.columns = ["OR_baseline", "CI_low_baseline", "CI_high_baseline", "p_baseline"]
cmp2.columns = ["OR_adjusted", "CI_low_adjusted", "CI_high_adjusted", "p_adjusted"]

comparison = cmp1.join(cmp2, how="outer")

print("\n=== PATTERN COMPARISON ===")
print(comparison)

comparison.to_csv("comparison_baseline_vs_adjusted_agecat.csv")
or2.to_csv("or_demographic_adjusted_agecat.csv")

print("\nSaved:")
print("- comparison_baseline_vs_adjusted_agecat.csv")
print("- or_demographic_adjusted_agecat.csv")