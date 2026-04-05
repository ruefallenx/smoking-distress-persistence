# Persistent Distress and Later Smoking Risk

This repository contains code and outputs for our CS208 Mini-PhD project on distress persistence and smoking risk using the PATH longitudinal survey.

## Project question

Our main question is:

**Is persistent distress more behaviorally relevant than temporary distress when predicting later smoking?**

Rather than treating distress as one single phenomenon, this project tests whether different distress trajectories across waves carry different levels of smoking risk.

## Main idea

We use repeated self-rated mental health measures to classify respondents into distress patterns across time:

- **low-low**: low distress at both waves
- **transient**: high distress only at Wave 6
- **emergent**: high distress only at Wave 7
- **persistent**: high distress at both waves

We then test whether these patterns predict **current smoking at Wave 7**.

## Data source

This project uses the **PATH Study public-use files**.

Main files used:

- Wave 5: `DS5001 / 36498-5001-Data.dta`
- Wave 6: `DS6001 / 36498-6001-Data.dta`
- Wave 7: `DS7001 / 36498-7001-Data.dta`

The analysis uses only variables available in the public-use dataset.

## Data access instructions

This repository does **not** include the original PATH `.dta` files.

To reproduce the analysis:

1. Obtain the PATH public-use data files.
2. Place them in a local folder structured like this:

```text
data/
  DS5001/
    36498-5001-Data.dta
  DS6001/
    36498-6001-Data.dta
  DS7001/
    36498-7001-Data.dta
```

3. Update file paths inside the scripts if your local directory is different.

Most scripts currently assume paths like:

```python
wave5_file = r"G:\Github\data\DS5001\36498-5001-Data.dta"
wave6_file = r"G:\Github\data\DS6001\36498-6001-Data.dta"
wave7_file = r"G:\Github\data\DS7001\36498-7001-Data.dta"
```

## Repository structure

```text
persistent-distress-path/
│
├─ README.md
├─ requirements.txt
│
├─ code/
│   ├─ main_fullsample_adjusted_agecat.py
│   ├─ subgroup_quit_attempt_adjusted_agecat.py
│   ├─ subgroup_baseline_smokers_adjusted_agecat.py
│   ├─ robustness_primary_quartile_3wave.py
│   └─ supporting/
│       ├─ support_check_measurement_variables.py
│       ├─ support_find_age_and_quit_variables.py
│       ├─ support_find_demographic_variables.py
│       ├─ support_measurement_distributions.py
│       ├─ support_measurement_value_labels.py
│       └─ support_validate_agecheck_vs_agecat.py
│
├─ results/
│   ├─ main/
│   ├─ robustness/
│   ├─ subgroups/
│   └─ supporting/
│
├─ figures/
│   ├─ main/
│   └─ robustness/
│
└─ data/
    └─ README_data_access.md
```

## Main scripts

### 1. `code/main_fullsample_adjusted_agecat.py`
Main full-sample model.

This script:
- merges Wave 6 and Wave 7
- defines high distress using the primary rule (**fair/poor = high distress**)
- creates 2-wave distress patterns
- recodes smoking status
- runs:
  - baseline-controlled model
  - demographic-adjusted model using:
    - age category
    - sex
    - education
    - income

Main outputs:
- `comparison_baseline_vs_adjusted_agecat.csv`
- `or_demographic_adjusted_agecat.csv`

### 2. `code/subgroup_quit_attempt_adjusted_agecat.py`
Quit-attempt subgroup model.

This script:
- identifies respondents reporting a quit attempt in the past 12 months
- creates the same distress patterns
- runs baseline-controlled and demographic-adjusted subgroup models

Main outputs:
- `comparison_quit_attempt_agecat_models.csv`
- `or_quit_attempt_adjusted_agecat.csv`

### 3. `code/subgroup_baseline_smokers_adjusted_agecat.py`
Baseline-smokers-only subgroup model.

This script:
- keeps only Wave 6 smokers
- creates the same distress patterns
- runs subgroup models to test whether Wave 7 smoking remains distinguishable in that subgroup

Main outputs:
- `comparison_smokers_only_agecat_models.csv`
- `or_smokers_only_adjusted_agecat.csv`
- `or_smokers_only_baseline.csv`

### 4. `code/robustness_primary_quartile_3wave.py`
Robustness and figure-generation script.

This script:
- runs the primary 2-wave definition (**4/5 = high distress**)
- runs a quartile-based sensitivity version
- runs a 3-wave persistence model using Waves 5–7
- generates the main figures

Main outputs:
- `comparison_primary_vs_quartile.csv`
- `comparison_2wave_primary_vs_3wave.csv`
- `OR_primary_fair_poor.csv`
- `OR_sensitivity_quartile.csv`
- `OR_3wave_persistence.csv`
- `pattern_counts_primary_fair_poor.csv`
- `pattern_counts_sensitivity_quartile.csv`
- `pattern_counts_3wave.csv`
- `crosstab_primary_pattern_smoker.csv`
- `crosstab_3wave_pattern_smoker.csv`

Main figures:
- `figure_primary_smoking_probability.png`
- `figure_primary_forest_plot.png`
- `figure_sensitivity_forest_plot.png`
- `figure_3wave_smoking_probability.png`
- `figure_3wave_forest_plot.png`

## Supporting scripts

These scripts were used to verify variables and measurement structure:

- `support_check_measurement_variables.py`
- `support_find_age_and_quit_variables.py`
- `support_find_demographic_variables.py`
- `support_measurement_distributions.py`
- `support_measurement_value_labels.py`
- `support_validate_agecheck_vs_agecat.py`

These are not required to reproduce the final figures, but they document how key variables were identified and checked.

## Reproducibility workflow

A third party can reproduce the main figures and tables by following this order:

### Step 1
Prepare the PATH public-use data in the expected folder structure.

### Step 2
Run the main model:

```bash
python code/main_fullsample_adjusted_agecat.py
```

### Step 3
Run subgroup checks:

```bash
python code/subgroup_quit_attempt_adjusted_agecat.py
python code/subgroup_baseline_smokers_adjusted_agecat.py
```

### Step 4
Run the robustness and figure script:

```bash
python code/robustness_primary_quartile_3wave.py
```

## Key final result

In the corrected demographic-adjusted full-sample model:

- **Persistent distress:** OR = 1.36, 95% CI [1.15, 1.62], p < .001
- **Emergent distress:** OR = 1.22, 95% CI [1.01, 1.47], p = .044
- **Transient distress:** OR = 1.15, 95% CI [0.95, 1.39], p = .162

This supports the main conclusion that **persistence, rather than one-time distress alone, is the more behaviorally meaningful smoking-risk signal** in this analysis.

## Notes

- This is an observational analysis, so results should be interpreted as **associations**, not causal effects.
- The distress measure is based on self-rated mental health and should be treated as an **anchor proxy**, not a clinical diagnosis.
- Earlier exploratory files and outputs were not included here as part of the final reproducible workflow.
