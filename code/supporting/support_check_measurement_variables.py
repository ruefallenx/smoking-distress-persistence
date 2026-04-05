# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 09:48:53 2026

@author: ruefa
"""

import pyreadstat
from pathlib import Path

root = Path(r"G:\github\data")
w6_file = root / "DS6001" / "36498-6001-Data.dta"
w7_file = root / "DS7001" / "36498-7001-Data.dta"

_, meta6 = pyreadstat.read_dta(str(w6_file), metadataonly=True)
_, meta7 = pyreadstat.read_dta(str(w7_file), metadataonly=True)

def show_vars(meta, targets, wave_name):
    print(f"\n=== {wave_name} ===")
    for var in targets:
        if var in meta.column_names:
            idx = meta.column_names.index(var)
            label = meta.column_labels[idx]
            print(f"{var} FOUND | label: {label}")
        else:
            print(f"{var} MISSING")

targets_w6 = ["R06_AX0091", "R06_AX0091_12M", "R06_AX0164"]
targets_w7 = ["R07_AX0091", "R07_AX0091_12M", "R07_AX0164"]

show_vars(meta6, targets_w6, "Wave 6")
show_vars(meta7, targets_w7, "Wave 7")