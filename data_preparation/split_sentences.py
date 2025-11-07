# Step 2: Split multi-sentence comments into single sentences
# Import necessary libraries
import pandas as pd
import spacy
import sys

# --- Configuration ---
INPUT_CSV = 'all_comments_cleaned.csv' # The output from Step 1
OUTPUT_CSV = 'all_comments_sentences.csv' # The new file for aspect extraction
TEXT_COLUMN = 'cleaned_text'             
# ---------------------

try:
    df = pd.read_csv(INPUT_CSV)
except FileNotFoundError:
    print(f"Error: Input file '{INPUT_CSV}' not found.") # Inform the user if the input file is missing
    sys.exit(1)

try:
    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Error: spaCy model 'en_core_web_sm' not found.") # Inform the user if the model is not found
    print("Please run: python -m spacy download en_core_web_sm") # Guide the user to download the model
    sys.exit(1)

print("Splitting multi-sentence comments into single sentences...")

single_sentences = []

# Iterate over each cleaned comment
for comment in df[TEXT_COLUMN].astype(str):
    doc = nlp(comment) # Process the comment with spaCy
    
    # doc.sents is a generator that finds each individual sentence
    for sentence in doc.sents:
        sent_text = sentence.text.strip() # Remove leading/trailing whitespace
        
        # Filter: Only keep sentences with more than 2 words.
        # This automatically removes "Apple.", "Lumi.", "Frangos.", "Oh perfect.", etc.
        if len(sent_text.split()) > 2: 
            single_sentences.append({'sentence_text': sent_text})

# Create a new DataFrame from the list of single sentences
df_sentences = pd.DataFrame(single_sentences)

# Save the new DataFrame to a CSV file
df_sentences.to_csv(OUTPUT_CSV, index=False)

print(f"\nStep 2 Complete: Split {len(df)} comments into {len(df_sentences)} sentences.")
print(f"New file created: '{OUTPUT_CSV}'")