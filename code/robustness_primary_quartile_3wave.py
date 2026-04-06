# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:32:04 2026

@author: ruefa
"""

import pandas as pd
import pyreadstat
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# =================================================
# 1. FILE PATHS
# =================================================

wave7_file = r"G:\github\data\DS7001\36498-7001-Data.dta"
wave6_file = r"G:\github\data\DS6001\36498-6001-Data.dta"
wave5_file = r"G:\github\data\DS5001\36498-5001-Data.dta"

# =================================================
# 2. HELPER FUNCTIONS
# =================================================

def find_var(df, keyword):
    for col in df.columns:
        if keyword in col:
            return col
    return None

def classify_pattern_2wave(high_w6, high_w7):
    if high_w6 and high_w7:
        return "persistent"
    elif high_w6 and not high_w7:
        return "transient_w6_only"
    elif not high_w6 and high_w7:
        return "emergent_w7_only"
    else:
        return "low_low"

def classify_pattern_3wave(distress_count):
    if distress_count >= 2:
        return "persistent"
    elif distress_count == 1:
        return "transient"
    else:
        return "low"

def run_logit_2wave(data, pattern_col, output_csv_name):
    temp = data.copy()

    temp[pattern_col] = pd.Categorical(
        temp[pattern_col],
        categories=["low_low", "transient_w6_only", "emergent_w7_only", "persistent"]
    )

    model = smf.logit(
        f"smoker_w7 ~ C({pattern_col}, Treatment(reference='low_low')) + smoker_w6",
        data=temp
    ).fit(disp=False)

    params = model.params
    conf = model.conf_int()

    results = pd.DataFrame({
        "OR": np.exp(params),
        "CI_low": np.exp(conf[0]),
        "CI_high": np.exp(conf[1]),
        "p_value": model.pvalues
    })

    print(f"\nOdds Ratios for {pattern_col}:")
    print(results)

    results.to_csv(output_csv_name)
    return model, results

def run_logit_3wave(data, pattern_col, output_csv_name):
    temp = data.copy()

    temp[pattern_col] = pd.Categorical(
        temp[pattern_col],
        categories=["low", "transient", "persistent"]
    )

    model = smf.logit(
        f"smoker_w7 ~ C({pattern_col}, Treatment(reference='low')) + smoker_w6",
        data=temp
    ).fit(disp=False)

    params = model.params
    conf = model.conf_int()

    results = pd.DataFrame({
        "OR": np.exp(params),
        "CI_low": np.exp(conf[0]),
        "CI_high": np.exp(conf[1]),
        "p_value": model.pvalues
    })

    print(f"\nOdds Ratios for {pattern_col}:")
    print(results)

    results.to_csv(output_csv_name)
    return model, results

def extract_pattern_rows_2wave(results_df, pattern_col_name):
    temp = results_df.copy()
    temp = temp[temp.index.str.contains(pattern_col_name, regex=False)].copy()

    labels = []
    for idx in temp.index:
        if "transient_w6_only" in idx:
            labels.append("transient")
        elif "emergent_w7_only" in idx:
            labels.append("emergent")
        elif "persistent" in idx:
            labels.append("persistent")
        else:
            labels.append(idx)

    temp.index = labels
    return temp[["OR", "CI_low", "CI_high", "p_value"]]

def extract_pattern_rows_3wave(results_df, pattern_col_name):
    temp = results_df.copy()
    temp = temp[temp.index.str.contains(pattern_col_name, regex=False)].copy()

    labels = []
    for idx in temp.index:
        if "transient" in idx:
            labels.append("transient")
        elif "persistent" in idx:
            labels.append("persistent")
        else:
            labels.append(idx)

    temp.index = labels
    return temp[["OR", "CI_low", "CI_high", "p_value"]]

def make_forest_plot_2wave(results_df, pattern_col_name, filename, title):
    forest = results_df.copy()
    forest = forest[forest.index.str.contains(pattern_col_name, regex=False)].copy()

    new_names = []
    for idx in forest.index:
        if "transient_w6_only" in idx:
            new_names.append("transient")
        elif "emergent_w7_only" in idx:
            new_names.append("emergent")
        elif "persistent" in idx:
            new_names.append("persistent")
        else:
            new_names.append(idx)

    forest.index = new_names
    display_order = ["transient", "emergent", "persistent"]
    forest = forest.reindex(display_order)

    or_vals = forest["OR"]
    ci_low = forest["CI_low"]
    ci_high = forest["CI_high"]

    err_low = or_vals - ci_low
    err_high = ci_high - or_vals

    plt.figure(figsize=(7, 4.5))
    plt.errorbar(
        or_vals,
        forest.index,
        xerr=[err_low, err_high],
        fmt="o"
    )
    plt.axvline(1)
    plt.xlabel("Odds Ratio for Current Smoking")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def make_forest_plot_3wave(results_df, pattern_col_name, filename, title):
    forest = results_df.copy()
    forest = forest[forest.index.str.contains(pattern_col_name, regex=False)].copy()

    new_names = []
    for idx in forest.index:
        if "transient" in idx:
            new_names.append("transient")
        elif "persistent" in idx:
            new_names.append("persistent")
        else:
            new_names.append(idx)

    forest.index = new_names
    display_order = ["transient", "persistent"]
    forest = forest.reindex(display_order)

    or_vals = forest["OR"]
    ci_low = forest["CI_low"]
    ci_high = forest["CI_high"]

    err_low = or_vals - ci_low
    err_high = ci_high - or_vals

    plt.figure(figsize=(7, 4.5))
    plt.errorbar(
        or_vals,
        forest.index,
        xerr=[err_low, err_high],
        fmt="o"
    )
    plt.axvline(1)
    plt.xlabel("Odds Ratio for Current Smoking")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

# =================================================
# 3. READ DATA
# =================================================

print("Loading Wave7...")
w7, meta7 = pyreadstat.read_dta(wave7_file, apply_value_formats=False)

print("Loading Wave6...")
w6, meta6 = pyreadstat.read_dta(wave6_file, apply_value_formats=False)

print("Loading Wave5...")
w5, meta5 = pyreadstat.read_dta(wave5_file, apply_value_formats=False)

print("W7 shape:", w7.shape)
print("W6 shape:", w6.shape)
print("W5 shape:", w5.shape)

# =================================================
# 4. AUTO FIND VARIABLES
# =================================================

w7_mh = find_var(w7, "AX0091")
w6_mh = find_var(w6, "AX0091")
w5_mh = find_var(w5, "AX0091")

w7_smoke = find_var(w7, "AC1003")
w6_smoke = find_var(w6, "AC1003")
w5_smoke = find_var(w5, "AC1003")

w7_quit = find_var(w7, "AC1010")
w6_quit = find_var(w6, "AC1010")

print("\nDetected variables:")
print("W7 MH:", w7_mh)
print("W6 MH:", w6_mh)
print("W5 MH:", w5_mh)
print("W7 smoke:", w7_smoke)
print("W6 smoke:", w6_smoke)
print("W5 smoke:", w5_smoke)
print("W7 quit:", w7_quit)
print("W6 quit:", w6_quit)

# =================================================
# 5. KEEP NECESSARY COLUMNS
# =================================================

w7_small = w7[["PERSONID", w7_mh, w7_smoke, w7_quit]].copy()
w6_small = w6[["PERSONID", w6_mh, w6_smoke, w6_quit]].copy()
w5_small = w5[["PERSONID", w5_mh, w5_smoke]].copy()

w7_small.columns = ["PERSONID", "mh_w7", "smoke_w7", "quit_w7"]
w6_small.columns = ["PERSONID", "mh_w6", "smoke_w6", "quit_w6"]
w5_small.columns = ["PERSONID", "mh_w5", "smoke_w5"]

# =================================================
# 6. MERGE WAVES
# =================================================

df = pd.merge(w6_small, w7_small, on="PERSONID", how="inner")

print("\nMerged 2-wave dataset shape:", df.shape)

print("\nDistribution of mh_w7:")
print(df["mh_w7"].value_counts().sort_index())

print("\nDistribution of mh_w6:")
print(df["mh_w6"].value_counts().sort_index())

# =================================================
# 7. CLEAN INVALID MH CODES
# Keep only valid MH responses 1..5
# =================================================

df = df[
    df["mh_w6"].isin([1, 2, 3, 4, 5]) &
    df["mh_w7"].isin([1, 2, 3, 4, 5])
].copy()

print("\nShape after removing invalid MH codes (2-wave):", df.shape)

# =================================================
# 8. PRIMARY 2-WAVE DEFINITION: HIGH DISTRESS = 4 OR 5
# =================================================

df["high_w6_primary"] = df["mh_w6"].isin([4, 5])
df["high_w7_primary"] = df["mh_w7"].isin([4, 5])

df["pattern_primary"] = df.apply(
    lambda row: classify_pattern_2wave(row["high_w6_primary"], row["high_w7_primary"]),
    axis=1
)

print("\nPRIMARY pattern counts (4/5 = high distress):")
primary_counts = df["pattern_primary"].value_counts()
print(primary_counts)

# =================================================
# 9. SENSITIVITY 2-WAVE DEFINITION: UPPER QUARTILE
# =================================================

threshold_w6 = df["mh_w6"].quantile(0.75)
threshold_w7 = df["mh_w7"].quantile(0.75)

print("\nQuartile thresholds:")
print("threshold_w6 =", threshold_w6)
print("threshold_w7 =", threshold_w7)

df["high_w6_quartile"] = df["mh_w6"] >= threshold_w6
df["high_w7_quartile"] = df["mh_w7"] >= threshold_w7

df["pattern_quartile"] = df.apply(
    lambda row: classify_pattern_2wave(row["high_w6_quartile"], row["high_w7_quartile"]),
    axis=1
)

print("\nSENSITIVITY pattern counts (quartile):")
quartile_counts = df["pattern_quartile"].value_counts()
print(quartile_counts)

# =================================================
# 10. RECODE 2-WAVE SMOKING OUTCOME
# PATH AC1003 coding used here:
# 1 / 2 = current smoker
# 3 / -1 = not current smoker
# Keep only valid codes: -1, 1, 2, 3
# =================================================

reg = df.copy()
reg = reg[reg["smoke_w7"].isin([-1, 1, 2, 3])]
reg = reg[reg["smoke_w6"].isin([-1, 1, 2, 3])].copy()

reg["smoker_w7"] = reg["smoke_w7"].isin([1, 2]).astype(int)
reg["smoker_w6"] = reg["smoke_w6"].isin([1, 2]).astype(int)

print("\nShape for 2-wave smoking models:", reg.shape)

# =================================================
# 11. RUN 2-WAVE LOGISTIC MODELS
# =================================================

model_primary, results_primary = run_logit_2wave(
    reg,
    "pattern_primary",
    "OR_primary_fair_poor.csv"
)

model_quartile, results_quartile = run_logit_2wave(
    reg,
    "pattern_quartile",
    "OR_sensitivity_quartile.csv"
)

# =================================================
# 12. SAVE 2-WAVE COUNTS AND CROSSTABS
# =================================================

primary_counts.to_csv("pattern_counts_primary_fair_poor.csv")
quartile_counts.to_csv("pattern_counts_sensitivity_quartile.csv")

ct_primary = pd.crosstab(
    reg["pattern_primary"],
    reg["smoker_w7"],
    normalize="index"
)

print("\nPRIMARY pattern x smoker_w7:")
print(ct_primary)

ct_primary.to_csv("crosstab_primary_pattern_smoker.csv")

# =================================================
# 13. 2-WAVE FIGURE: SMOKING PROBABILITY (FINAL CLEAN VERSION)
# =================================================

plot_df = reg.copy()

# Step 1: calculate probability
prob = plot_df.groupby("pattern_primary")["smoker_w7"].mean()

# Step 2: reorder (VERY IMPORTANT)
prob = prob[[
    "low_low",
    "transient_w6_only",
    "emergent_w7_only",
    "persistent"
]]

# Step 3: rename labels (VERY IMPORTANT)
prob.index = ["Low", "Transient", "Emergent", "Persistent"]

# Step 4: plot (presentation style)
plt.figure(figsize=(8, 5))

bars = plt.bar(prob.index, prob.values)

plt.ylabel("Probability of Current Smoking (Wave 7)")
plt.xlabel("Distress Pattern")
plt.title("Primary Definition: Distress Pattern and Smoking Probability")

plt.xticks(rotation=0)

# Optional: add value labels on bars (VERY NICE for presentation)
for i, v in enumerate(prob.values):
    plt.text(i, v + 0.005, f"{v:.2f}", ha='center')

plt.tight_layout()

plt.savefig("figure_primary_smoking_probability_clean.png", dpi=300)

plt.show()
# =================================================
# 14. 2-WAVE FOREST PLOTS
# =================================================

make_forest_plot_2wave(
    results_primary,
    "pattern_primary",
    "figure_primary_forest_plot.png",
    "Primary Definition: Effect of Distress Pattern on Smoking"
)

make_forest_plot_2wave(
    results_quartile,
    "pattern_quartile",
    "figure_sensitivity_forest_plot.png",
    "Sensitivity Check: Quartile Definition"
)

# =================================================
# 15. 2-WAVE COMPARISON TABLE
# =================================================

primary_comp = extract_pattern_rows_2wave(results_primary, "pattern_primary")
quartile_comp = extract_pattern_rows_2wave(results_quartile, "pattern_quartile")

comparison = primary_comp.join(
    quartile_comp,
    lsuffix="_primary",
    rsuffix="_quartile"
)

print("\nComparison table: PRIMARY vs QUARTILE")
print(comparison)

comparison.to_csv("comparison_primary_vs_quartile.csv")

# =================================================
# 16. 3-WAVE MERGE
# =================================================

df3 = pd.merge(df, w5_small, on="PERSONID", how="inner")

print("\nMerged 3-wave dataset shape:", df3.shape)

print("\nDistribution of mh_w5:")
print(df3["mh_w5"].value_counts().sort_index())

# =================================================
# 17. CLEAN INVALID MH CODES FOR 3-WAVE
# =================================================

df3 = df3[
    df3["mh_w5"].isin([1, 2, 3, 4, 5]) &
    df3["mh_w6"].isin([1, 2, 3, 4, 5]) &
    df3["mh_w7"].isin([1, 2, 3, 4, 5])
].copy()

print("\nShape after removing invalid MH codes (3-wave):", df3.shape)

# =================================================
# 18. 3-WAVE DISTRESS PERSISTENCE INDEX
# High distress = 4 or 5 in each wave
# persistent = 2+ waves high
# transient = 1 wave high
# low = 0 waves high
# =================================================

df3["high_w5"] = df3["mh_w5"].isin([4, 5])
df3["high_w6"] = df3["mh_w6"].isin([4, 5])
df3["high_w7"] = df3["mh_w7"].isin([4, 5])

df3["distress_count"] = (
    df3["high_w5"].astype(int) +
    df3["high_w6"].astype(int) +
    df3["high_w7"].astype(int)
)

df3["pattern_3wave"] = df3["distress_count"].apply(classify_pattern_3wave)

print("\n3-wave pattern counts:")
pattern3_counts = df3["pattern_3wave"].value_counts()
print(pattern3_counts)

pattern3_counts.to_csv("pattern_counts_3wave.csv")

# =================================================
# 19. RECODE 3-WAVE SMOKING OUTCOME
# Model outcome remains Wave 7 smoking, controlling Wave 6 smoking
# =================================================

reg3 = df3.copy()
reg3 = reg3[reg3["smoke_w7"].isin([-1, 1, 2, 3])]
reg3 = reg3[reg3["smoke_w6"].isin([-1, 1, 2, 3])].copy()

reg3["smoker_w7"] = reg3["smoke_w7"].isin([1, 2]).astype(int)
reg3["smoker_w6"] = reg3["smoke_w6"].isin([1, 2]).astype(int)

print("\nShape for 3-wave smoking model:", reg3.shape)

# =================================================
# 20. RUN 3-WAVE LOGISTIC MODEL
# =================================================

model3, results3 = run_logit_3wave(
    reg3,
    "pattern_3wave",
    "OR_3wave_persistence.csv"
)

# =================================================
# 21. 3-WAVE CROSSTAB
# =================================================

ct_3wave = pd.crosstab(
    reg3["pattern_3wave"],
    reg3["smoker_w7"],
    normalize="index"
)

print("\n3-wave pattern x smoker_w7:")
print(ct_3wave)

ct_3wave.to_csv("crosstab_3wave_pattern_smoker.csv")

# =================================================
# 22. 3-WAVE FIGURE: SMOKING PROBABILITY
# =================================================

prob3 = reg3.groupby("pattern_3wave")["smoker_w7"].mean()
order3 = ["low", "transient", "persistent"]
prob3 = prob3.reindex(order3)

plt.figure(figsize=(7, 5))
plt.bar(prob3.index, prob3.values)
plt.ylabel("Probability of Current Smoking (Wave 7)")
plt.xlabel("3-Wave Distress Pattern")
plt.title("3-Wave Persistence Index and Smoking Probability")
plt.tight_layout()
plt.savefig("figure_3wave_smoking_probability.png", dpi=300)
plt.show()

# =================================================
# 23. 3-WAVE FOREST PLOT
# =================================================

make_forest_plot_3wave(
    results3,
    "pattern_3wave",
    "figure_3wave_forest_plot.png",
    "3-Wave Persistence Index: Effect on Smoking"
)

# =================================================
# 24. OPTIONAL COMPARISON: 2-WAVE PRIMARY VS 3-WAVE
# =================================================

comp2 = extract_pattern_rows_2wave(results_primary, "pattern_primary")
comp3 = extract_pattern_rows_3wave(results3, "pattern_3wave")

comparison_2v3 = comp2.join(
    comp3,
    lsuffix="_2wave_primary",
    rsuffix="_3wave",
    how="outer"
)

print("\nComparison table: 2-wave primary vs 3-wave")
print(comparison_2v3)

comparison_2v3.to_csv("comparison_2wave_primary_vs_3wave.csv")

# =================================================
# 25. DONE
# =================================================

print("\nAll files saved.")
print("Main outputs:")
print("- pattern_counts_primary_fair_poor.csv")
print("- pattern_counts_sensitivity_quartile.csv")
print("- pattern_counts_3wave.csv")
print("- OR_primary_fair_poor.csv")
print("- OR_sensitivity_quartile.csv")
print("- OR_3wave_persistence.csv")
print("- comparison_primary_vs_quartile.csv")
print("- comparison_2wave_primary_vs_3wave.csv")
print("- figure_primary_smoking_probability.png")
print("- figure_primary_forest_plot.png")
print("- figure_sensitivity_forest_plot.png")
print("- figure_3wave_smoking_probability.png")
print("- figure_3wave_forest_plot.png")

print("\nMost important things to check after running:")
print("1. print(primary_counts)")
print("2. print(results_primary)")
print("3. print(pattern3_counts)")
print("4. print(results3)")