# smoking-distress-persistence

Mini-PhD project examining whether **persistent psychological distress** is more strongly associated with **continued smoking** than temporary distress, using the **PATH Study public-use data**.

## Research question

Does persistent psychological distress across time matter more than temporary distress for predicting continued smoking behavior?

## Project summary

Many studies look at distress after quitting or during smoking behavior, but they often treat distress as a single-time-point condition. This project tests whether a **repeated or persistent distress pattern** is more behaviorally meaningful than a temporary pattern.

Using longitudinal PATH data, distress was classified across waves into four groups:

- **low**: low distress at both time points
- **transient**: high distress at the earlier wave only
- **emergent**: high distress at the later wave only
- **persistent**: high distress at both waves

The main outcome is continued smoking at Wave 7.

## Main finding

In the demographic-adjusted full-sample model, **persistent distress remained significantly associated with Wave 7 smoking**, while transient and emergent distress were weaker and not consistently significant across specifications.

## Dataset

This project uses the **Population Assessment of Tobacco and Health (PATH) Study, Public-Use Files**.

Waves used in this repository:

- **Wave 5**
- **Wave 6**
- **Wave 7**

## Important note on data access

Raw PATH data are **not included** in this repository.

To reproduce the analysis, obtain the PATH public-use files separately and place them in your local machine. See the instructions in:

- `data_access/how_to_get_path_data.txt`

## Repository structure

```text
smoking-distress-persistence/
├── README.md
├── requirements.txt
├── code/
├── figures/
├── results/
└── data_access/
```

### Folder descriptions

- `code/` — Python analysis scripts for main, subgroup, and robustness analyses
- `figures/` — output figures used for interpretation and presentation
- `results/` — saved analysis outputs and tables
- `data_access/` — instructions for obtaining PATH data and setting local paths
- `requirements.txt` — Python package dependencies

## Main scripts

Examples of key scripts in `code/` include:

- `main_fullsample_adjusted_agecat.py`
- `subgroup_quit_attempt_adjusted_agecat.py`
- `subgroup_baseline_smokers_adjusted_agecat.py`
- `robustness_primary_quartile_3wave.py`

These scripts correspond to:

- the main full-sample adjusted model
- subgroup analyses
- robustness checks using alternative distress definitions

## How to run

Install dependencies first:

```bash
pip install -r requirements.txt
```

Then run scripts from the repository root, for example:

```bash
python code/main_fullsample_adjusted_agecat.py
python code/subgroup_quit_attempt_adjusted_agecat.py
python code/subgroup_baseline_smokers_adjusted_agecat.py
python code/robustness_primary_quartile_3wave.py
```

## Local path note

Some scripts use local example file paths for the PATH data files.  
Before running them, update those paths on your machine so they point to your local PATH dataset location.

## Reproducibility note

This repository is intended to provide:

- the analysis code
- the figure outputs
- the result files
- the data access instructions

Because the PATH raw files are not redistributed here, a user must download the public-use dataset independently before reproducing the analyses.

## Authors

- Hui Geng
- Oussama Msehli

## Course context

This repository was prepared for a **CS208 Mini-PhD project** on smoking behavior and distress persistence.
