# Convert agreed and resolved annotations into .raw format for model training and testing.
# Import necessary libraries
import pandas as pd
import sys

# --- Configuration ---
AGREEMENTS_FILE = 'agreements.csv'
RESOLVED_FILE = 'disagreements_to_fix.csv' # The manually-fixed file

TRAIN_OUTPUT_FILE = 'reddit_train.raw'
TEST_OUTPUT_FILE = 'reddit_test.raw'

TRAIN_SPLIT_RATIO = 0.8 # 80% for training, 20% for testing
RANDOM_SEED = 42      # Use a seed for reproducible shuffles
# ---------------------

try:
    df_agreed = pd.read_csv(AGREEMENTS_FILE)
    df_resolved = pd.read_csv(RESOLVED_FILE)
except FileNotFoundError as e:
    print(f"Error: Could not find files. Run find_disagreements.py and fix the disagreements") # Inform the user about missing files
    print(e)
    sys.exit(1)

# Check if you filled in the final polarity
if 'final_polarity' not in df_resolved.columns:
    print("Error: The file 'disagreements_to_fix.csv' is missing the 'final_polarity' column.")
    print("Please complete the manual adjudication step first.")
    sys.exit(1)

# Check for missing values in the 'final_polarity' column
if df_resolved['final_polarity'].isnull().any():
    print("Error: You have missing values in the 'final_polarity' column. Please fill them all in.")
    sys.exit(1)

# Standardize the resolved file to match the agreed file
df_resolved['polarity'] = df_resolved['final_polarity']
df_resolved_final = df_resolved[['sentence', 'aspect_term', 'polarity']]

# Combine the two dataframes
df_final = pd.concat([df_agreed, df_resolved_final], ignore_index=True)

print(f"Successfully combined {len(df_agreed)} agreed annotations and {len(df_resolved_final)} resolved annotations.")
print(f"Total annotations: {len(df_final)}")

# Shuffle the data
print("Shuffling the dataset...")
df_final = df_final.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

# Split the data into training and testing sets
split_index = int(len(df_final) * TRAIN_SPLIT_RATIO)
df_train = df_final.iloc[:split_index]
df_test = df_final.iloc[split_index:]

print(f"Splitting into {len(df_train)} train samples and {len(df_test)} test samples.")

# --- Polarity mapping dictionary ---
polarity_map = {
    'positive': 1,
    'negative': -1,
    'neutral': 0
}

# --- Helper function to write .raw files ---
def write_to_raw(dataframe, filename):
    count = 0
    # Open the file for writing
    with open(filename, 'w', encoding='utf-8') as f:
        for index, row in dataframe.iterrows():
            sentence = str(row['sentence']) # Original sentence
            aspect_term = str(row['aspect_term']) # Aspect term
            polarity_str = str(row['polarity']).strip().lower() # Polarity as string
            
            # Map polarity string to integer
            if polarity_str in polarity_map: 
                polarity = polarity_map[polarity_str]
            else:
                print(f"Warning: Unknown polarity '{row['polarity']}' in {filename}. Skipping row {index}.") # Warn and skip unknown polarities
                continue
                
            try:
                placeholder_sentence = sentence.replace(aspect_term, '$T$', 1) # Replace first occurrence only
            except Exception:
                placeholder_sentence = sentence  # Fallback in case of error

            # Write the processed lines to the file
            f.write(placeholder_sentence.strip() + '\n')
            f.write(aspect_term.lower().strip() + '\n')
            f.write(str(polarity) + '\n')
            count += 1
    print(f"Successfully wrote {count} entries to '{filename}'.")

# --- Write both files ---
write_to_raw(df_train, TRAIN_OUTPUT_FILE)
write_to_raw(df_test, TEST_OUTPUT_FILE)

print("\nDone. Final train and test .raw files created.")
print("Data construction is complete.")