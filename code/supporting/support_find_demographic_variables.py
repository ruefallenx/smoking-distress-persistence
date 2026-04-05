# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:17:34 2026

@author: ruefa
"""

import pyreadstat
import pandas as pd

# =================================================
# FILE PATH
# =================================================
wave6_file = r"G:\Github\data\DS6001\36498-6001-Data.dta"

# =================================================
# LOAD METADATA ONLY
# =================================================
print("Loading Wave 6 metadata...")
_, meta = pyreadstat.read_dta(
    wave6_file,
    metadataonly=True,
    apply_value_formats=False
)

# =================================================
# BUILD SEARCHABLE TABLE
# =================================================
df_vars = pd.DataFrame({
    "var_name": meta.column_names,
    "label": meta.column_labels
})

df_vars["label"] = df_vars["label"].fillna("")
df_vars["var_lower"] = df_vars["var_name"].str.lower()
df_vars["label_lower"] = df_vars["label"].str.lower()

# =================================================
# SEARCH FUNCTION
# =================================================
def search_vars(keywords, title):
    print("\n" + "="*70)
    print(title)
    print("="*70)

    mask = False
    for kw in keywords:
        mask = mask | df_vars["var_lower"].str.contains(kw.lower(), na=False) \
                    | df_vars["label_lower"].str.contains(kw.lower(), na=False)

    result = df_vars.loc[mask, ["var_name", "label"]].drop_duplicates()

    if result.empty:
        print("No matches found.")
    else:
        print(result.to_string(index=False))

# =================================================
# SEARCH TARGETS
# =================================================
search_vars(
    ["age", "old", "birth"],
    "AGE CANDIDATES"
)

search_vars(
    ["sex", "gender", "male", "female"],
    "SEX / GENDER CANDIDATES"
)

search_vars(
    ["education", "school", "degree", "college", "grade"],
    "EDUCATION CANDIDATES"
)

search_vars(
    ["income", "poverty", "household income", "family income", "earnings", "salary"],
    "INCOME / POVERTY CANDIDATES"
)

# Optional: save to csv
df_vars.to_csv("wave6_all_variables_with_labels.csv", index=False)
print("\nSaved full variable list to wave6_all_variables_with_labels.csv")