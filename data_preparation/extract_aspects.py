# Step 3: Extract Aspect Term Candidates from Sentences
# Import necessary libraries
import pandas as pd
import spacy
import sys

# --- Configuration ---
INPUT_CSV = 'all_comments_sentences.csv' # The output from Step 2
OUTPUT_CSV = 'annotation_tasks.csv'      # The final file for annotation
TEXT_COLUMN = 'sentence_text'            
# ---------------------

try:
    df = pd.read_csv(INPUT_CSV)
except FileNotFoundError:
    print(f"Error: Input file '{INPUT_CSV}' not found.") # Inform the user if the input file is missing
    sys.exit(1)

try:
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Error: spaCy model 'en_core_web_sm' not found.") # Inform the user if the spaCy model is missing
    sys.exit(1)

tasks = []

print("Extracting aspect term candidates (noun chunks) from sentences...")

# Process each single sentence
for text in df[TEXT_COLUMN].astype(str):
    doc = nlp(text)
    
    # Extract all noun chunks as potential aspect terms
    for chunk in doc.noun_chunks:
        aspect = chunk.text.lower().strip()
        
        # Filter: ignore pronouns and very short terms
        if len(aspect) > 2 and aspect not in ['he', 'she', 'it', 'they', 'i', 'you', 'we']:
            tasks.append({'sentence': text, 'aspect_term': aspect})

# Create a new DataFrame with the tasks
df_tasks = pd.DataFrame(tasks)

# Remove duplicate sentence/aspect pairs
df_tasks.drop_duplicates(inplace=True)

# Shuffle the data randomly
print(f"Found {len(df_tasks)} tasks. Shuffling them randomly...")
df_tasks = df_tasks.sample(frac=1).reset_index(drop=True)

# Save to a new CSV
df_tasks.to_csv(OUTPUT_CSV, index=False)

print(f"\nStep 3 Complete: Extracted and shuffled {len(df_tasks)} aspect tasks.")
print(f"New file created: '{OUTPUT_CSV}'")