# Calculate Inter-Annotator Agreement (IAA) using Cohen's Kappa
# Import necessary libraries
import pandas as pd
from sklearn.metrics import cohen_kappa_score
import sys

# --- Configuration ---
FILE_1 = 'annotator_1.csv'
FILE_2 = 'annotator_2.csv'
LABEL_COLUMN = 'polarity'
# ---------------------

try:
    df1 = pd.read_csv(FILE_1)
    df2 = pd.read_csv(FILE_2)
except FileNotFoundError as e:
    print(f"Error: Could not find file. Make sure '{FILE_1}' and '{FILE_2}' are in the directory.") # Inform the user if the files are missing
    print(e)
    sys.exit(1)

# Check if files are the same length
if len(df1) != len(df2):
    print(f"Error: Files have different lengths ({len(df1)} vs {len(df2)}). Cannot compare.")
    sys.exit(1)

# Check for missing values (in case an annotator missed one)
if df1[LABEL_COLUMN].isnull().any() or df2[LABEL_COLUMN].isnull().any():
    print("Warning: Missing values found. Dropping rows with missing labels for comparison.")
    df1 = df1.dropna(subset=[LABEL_COLUMN])
    df2 = df2.dropna(subset=[LABEL_COLUMN])
    # Re-align dataframes by index after dropping
    common_index = df1.index.intersection(df2.index)
    df1 = df1.loc[common_index]
    df2 = df2.loc[common_index]

# Get the lists of labels
labels_1 = df1[LABEL_COLUMN]
labels_2 = df2[LABEL_COLUMN]

# Calculate Cohen's Kappa
kappa = cohen_kappa_score(labels_1, labels_2)

print(f"--- Inter-Annotator Agreement (IAA) ---")
print(f"Compared {len(labels_1)} annotations.")
print(f"Cohen's Kappa Score: {kappa:.4f}")
print("------------------------------------------")