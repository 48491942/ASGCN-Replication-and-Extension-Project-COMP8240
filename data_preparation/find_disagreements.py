# Find Disagreements Between Two Annotators' CSV Files
# Import necessary libraries
import pandas as pd
import sys

# --- Configuration ---
FILE_1 = 'annotator_1.csv'
FILE_2 = 'annotator_2.csv'

# Columns to check
SENTENCE_COL = 'sentence'
ASPECT_COL = 'aspect_term'
LABEL_COL = 'polarity'
# ---------------------

try:
    df1 = pd.read_csv(FILE_1)
    df2 = pd.read_csv(FILE_2)
except FileNotFoundError as e:
    print(f"Error: Could not find file. Make sure '{FILE_1}' and '{FILE_2}' are in the directory.") # Inform the user about the missing files
    sys.exit(1)

# Make sure the files are aligned (this assumes they have the same rows in the same order)
if len(df1) != len(df2):
    print("Error: Files are not the same length. Cannot compare.")
    sys.exit(1)

# Add columns to show each annotator's label
df1['annotator_1_label'] = df1[LABEL_COL]
df2['annotator_2_label'] = df2[LABEL_COL]

# Merge the dataframes on the key columns
df_merged = pd.merge(
    df1[[SENTENCE_COL, ASPECT_COL, 'annotator_1_label']],
    df2[[SENTENCE_COL, ASPECT_COL, 'annotator_2_label']],
    on=[SENTENCE_COL, ASPECT_COL],
    how='inner'
)

# Find disagreements
disagreements = df_merged[df_merged['annotator_1_label'] != df_merged['annotator_2_label']].copy()

# Find agreements
agreements = df_merged[df_merged['annotator_1_label'] == df_merged['annotator_2_label']].copy()

# --- Save Files ---
if disagreements.empty:
    print("No disagreements found!")
else:
    disagreements.to_csv('disagreements_to_fix.csv', index=False)
    print(f"Found {len(disagreements)} disagreements.")

if not agreements.empty:
    # We only need one label column for the agreed-upon file
    agreements['polarity'] = agreements['annotator_1_label']
    agreements_final = agreements[[SENTENCE_COL, ASPECT_COL, 'polarity']]
    agreements_final.to_csv('agreements.csv', index=False)
    print(f"Saved {len(agreements)} agreed-upon annotations to 'agreements.csv'.")
