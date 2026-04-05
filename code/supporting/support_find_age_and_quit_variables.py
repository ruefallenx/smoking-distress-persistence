# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:34:46 2026

@author: ruefa
"""

import pyreadstat
import pandas as pd

# =================================================
# FILE PATH
# =================================================
wave6_file = r"G:\Github\data\DS6001\36498-6001-Data.dta"
wave7_file = r"G:\Github\data\DS7001\36498-7001-Data.dta"

# =================================================
# LOAD METADATA ONLY
# =================================================
print("Loading Wave 6 metadata...")
_, meta6 = pyreadstat.read_dta(
    wave6_file,
    metadataonly=True,
    apply_value_formats=False
)

print("Loading Wave 7 metadata...")
_, meta7 = pyreadstat.read_dta(
    wave7_file,
    metadataonly=True,
    apply_value_formats=False
)

def make_df(meta, wave_label):
    return pd.DataFrame({
        "wave": wave_label,
        "var_name": meta.column_names,
        "label": meta.column_labels
    })

df6 = make_df(meta6, "W6")
df7 = make_df(meta7, "W7")

df = pd.concat([df6, df7], ignore_index=True)
df["label"] = df["label"].fillna("")
df["var_lower"] = df["var_name"].str.lower()
df["label_lower"] = df["label"].str.lower()

# =================================================
# SEARCH FUNCTION
# =================================================
def search_vars(keywords, title):
    print("\n" + "="*80)
    print(title)
    print("="*80)

    mask = False
    for kw in keywords:
        mask = mask | df["var_lower"].str.contains(kw.lower(), na=False) \
                    | df["label_lower"].str.contains(kw.lower(), na=False)

    result = df.loc[mask, ["wave", "var_name", "label"]].drop_duplicates()

    if result.empty:
        print("No matches found.")
    else:
        print(result.to_string(index=False))

# =================================================
# 1. AGE SEARCH
# =================================================
search_vars(
    ["age at interview", "age in years", "respondent age", "age", "age range"],
    "AGE CANDIDATES"
)

# =================================================
# 2. QUIT / CESSATION SEARCH
# =================================================
search_vars(
    ["quit", "stopped smoking", "trying to quit", "tried to quit", "quit attempt",
     "attempt to quit", "past 12 months quit", "completely quit", "gave up", "stopped"],
    "QUIT / CESSATION CANDIDATES"
)

# =================================================
# 3. INTENTION / PLAN TO QUIT SEARCH
# =================================================
search_vars(
    ["plan to quit", "intend to quit", "thinking about quitting",
     "seriously considering quitting", "want to quit", "goal is to quit"],
    "QUIT INTENTION CANDIDATES"
)

# =================================================
# 4. RECENT FORMER / LAST SMOKED SEARCH
# =================================================
search_vars(
    ["last smoked", "how long ago", "former smoker", "ex-smoker",
     "days since", "when did you stop", "time since quit"],
    "RECENCY / FORMER SMOKER CANDIDATES"
)

# Optional full export
df.to_csv("wave6_wave7_all_variables_with_labels.csv", index=False)
print("\nSaved full variable list to wave6_wave7_all_variables_with_labels.csv")