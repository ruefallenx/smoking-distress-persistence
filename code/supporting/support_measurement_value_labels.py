# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 09:58:10 2026

@author: ruefa
"""

import pyreadstat
from pathlib import Path

root = Path(r"G:\github\data")
w6_file = root / "DS6001" / "36498-6001-Data.dta"
w7_file = root / "DS7001" / "36498-7001-Data.dta"

usecols_w6 = ["R06_AX0091_12M", "R06_AX0164"]
usecols_w7 = ["R07_AX0091_12M", "R07_AX0164"]

print("Loading W6 with value labels...")
w6, _ = pyreadstat.read_dta(
    str(w6_file),
    usecols=usecols_w6,
    apply_value_formats=True
)

print("Loading W7 with value labels...")
w7, _ = pyreadstat.read_dta(
    str(w7_file),
    usecols=usecols_w7,
    apply_value_formats=True
)

def show_dist(df, var):
    print(f"\n=== {var} ===")
    print(df[var].value_counts(dropna=False))

print("\n########## WAVE 6 ##########")
for var in usecols_w6:
    show_dist(w6, var)

print("\n########## WAVE 7 ##########")
for var in usecols_w7:
    show_dist(w7, var)