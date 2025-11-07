# Step 1: Clean and combine raw comment data
# Import necessary libraries
import pandas as pd
import ftfy # for fixing text encoding issues
import re
import sys
import glob

# --- Configuration ---
# Use glob to find all the raw comment files.
# This assumes that the CSVs are in a folder named 'raw_data'
input_files = glob.glob('raw_data/*.csv')
output_file = 'all_comments_cleaned.csv'
# This is the name of the column in the CSVs that contains the comments
COMMENT_COLUMN_NAME = 'comment_text' 
# ---------------------

# --- Cleaning Function ---
def clean_text(text):
    """
    Applies a series of cleaning steps to a single piece of text.
    """
    # 1. Fix encoding errors (e.g., 'â€™' -> ''')
    text = ftfy.fix_text(text)
    
    # 2. Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 3. Remove Reddit user/subreddit mentions (u/ and r/)
    text = re.sub(r'u/\w+|r/\w+', '', text)
    
    # 4. Remove special tokens and junk
    text = re.sub(r'\[deleted\]|\[removed\]|#NAME\?', '', text, flags=re.IGNORECASE)
    
    # 5. Convert to lowercase
    text = text.lower()
    
    # 6. Remove non-alphanumeric/punctuation (keeps letters, numbers, and basic punctuation)
    # This will remove most emojis like 'ðŸ¥²'
    text = re.sub(r'[^a-z0-9\s.,\'"-]', '', text)
    
    # 7. Normalize whitespace (replaces newlines, tabs, and multiple spaces with a single space)
    # This fixes multi-line comments.
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# --- Main execution ---
if not input_files:
    # If no files found, inform the user and exit
    print("Error: No CSV files found in the 'raw_data' folder.")
    print("Please create a folder named 'raw_data' and put your CSVs in it.")
    sys.exit(1)

print(f"Found {len(input_files)} files to combine and clean.")

# Read and combine all CSV files
all_dfs = []
for f in input_files:
    try:
        # Read each CSV file
        df = pd.read_csv(f)
        if COMMENT_COLUMN_NAME not in df.columns:
            print(f"Warning: '{COMMENT_COLUMN_NAME}' not in {f}. Skipping this file.") # Warn if column not found
            continue
        all_dfs.append(df) # Append dataframe to list
    except Exception as e:
        print(f"Error reading {f}: {e}")

# Check if any dataframes were read
if not all_dfs:
    print("Error: No valid data could be read. Please check your CSV files and column name.")
    sys.exit(1)

# Combine all dataframes into one
df_combined = pd.concat(all_dfs, ignore_index=True)

print(f"Total raw comments found: {len(df_combined)}")

# Clean the text
df_combined['cleaned_text'] = df_combined[COMMENT_COLUMN_NAME].astype(str).apply(clean_text)

# Save to a new, clean file
df_combined.to_csv(output_file, index=False)

print(f"\nStep 1 Complete: All comments combined and cleaned.")
print(f"New file created: '{output_file}'")
print(f"Total comments processed: {len(df_combined)}")