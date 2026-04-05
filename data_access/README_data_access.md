PATH DATA ACCESS INSTRUCTIONS

Project:
Distress Persistence and Later Smoking Risk: A Longitudinal Analysis Using PATH Data

Data source:
Population Assessment of Tobacco and Health (PATH) Study
Public-use files
ICPSR 36498

Waves used in this project:
- Wave 5
- Wave 6
- Wave 7

How to obtain the data:
1. Visit the ICPSR page for the PATH public-use files (ICPSR 36498).
2. Download the PATH public-use dataset package.
3. Extract the files to a local folder on your computer.

Important:
The raw PATH data are not included in this repository.
Users must obtain the PATH public-use files directly from ICPSR.

Local directory note:
In our local setup, the extracted ICPSR package contains many folders in the original ICPSR format, including Wave 5–7 folders in the 5000–7000 series.
For simplicity, users should download and extract the full PATH public-use package rather than trying to isolate only specific subfolders.

Path note:
File names and local paths may vary depending on how the ICPSR package is extracted on each machine.
If needed, update file paths in the Python scripts before running them.

Main variables used:
- PERSONID (merge key)
- AX0091 (self-rated mental health)
- AC1003 (current smoking)
- smoking / quit-attempt-related variables used in subgroup analyses
- demographic variables for age category, sex, education, and household income

Recommended reproduction order:
1. Run the merge and cleaning script.
2. Run the main analysis script.
3. Run subgroup and robustness scripts if needed.
4. Run the figure-generation script.

For the full project overview and script order, see the README file.