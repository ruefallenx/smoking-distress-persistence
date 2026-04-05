# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 09:51:26 2026

@author: ruefa
"""

import pyreadstat
import pandas as pd
from pathlib import Path

root = Path(r"G:\github\data")
w6_file = root / "DS6001" / "36498-6001-Data.dta"
w7_file = root / "DS7001" / "36498-7001-Data.dta"

usecols_w6 = ["R06_AX0091", "R06_AX0091_12M", "R06_AX0164"]
usecols_w7 = ["R07_AX0091", "R07_AX0091_12M", "R07_AX0164"]

print("Loading Wave 6 minimal measurement columns...")
w6, meta6 = pyreadstat.read_dta(
    str(w6_file),
    usecols=usecols_w6,
    apply_value_formats=False
)

print("Loading Wave 7 minimal measurement columns...")
w7, meta7 = pyreadstat.read_dta(
    str(w7_file),
    usecols=usecols_w7,
    apply_value_formats=False
)

def show_distribution(df, var, label):
    print(f"\n=== {var} ===")
    print("Label:", label)
    vc = df[var].value_counts(dropna=False).sort_index()
    print(vc)

print("\n================ WAVE 6 ================")
for var, label in zip(meta6.column_names, meta6.column_labels):
    show_distribution(w6, var, label)

print("\n================ WAVE 7 ================")
for var, label in zip(meta7.column_names, meta7.column_labels):
    show_distribution(w7, var, label)