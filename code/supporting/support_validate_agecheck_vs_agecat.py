# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:39:38 2026

@author: ruefa
"""

import pyreadstat
import pandas as pd

wave6_file = r"G:\Github\data\DS6001\36498-6001-Data.dta"

usecols = ["PERSONID", "R06R_A_AGE_CHECK", "R06R_A_AGECAT6"]

df, meta = pyreadstat.read_dta(
    wave6_file,
    usecols=usecols,
    apply_value_formats=False
)

print("AGE_CHECK distribution:")
print(df["R06R_A_AGE_CHECK"].value_counts(dropna=False).sort_index())

print("\nAGECAT6 distribution:")
print(df["R06R_A_AGECAT6"].value_counts(dropna=False).sort_index())

print("\nAGE_CHECK summary:")
print(df["R06R_A_AGE_CHECK"].describe())