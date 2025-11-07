# Convert XML-formatted data to 3-line .raw format for ASGCN
# Import necessary libraries
import xml.etree.ElementTree as ET # for XML parsing
import sys

def convert_xml(input_file, output_file):
    """
    Converts an XML-formatted file to the 3-line .raw format for ASGCN.
    """
    try:
        # Parse the XML file
        tree = ET.parse(input_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}") # Print parsing error
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.") # Print file not found error
        sys.exit(1)

    # Polarity mapping
    polarity_map = {
        'positive': 1,
        'neutral': 0,
        'negative': -1
    }
    
    # Open output file for writing
    entry_count = 0
    with open(output_file, 'w', encoding='utf-8') as f_out:
        # Iterate over each sentence in the XML
        for sentence_elem in root.findall('sentence'):
            original_text = sentence_elem.find('text').text # Get the original sentence text
            
            aspect_terms_elem = sentence_elem.find('aspectTerms') # Get aspect terms element
            if aspect_terms_elem is None:
                continue

            for aspect_term_elem in aspect_terms_elem.findall('aspectTerm'):
                term = aspect_term_elem.get('term') # Get the aspect term
                polarity_str = aspect_term_elem.get('polarity') # Get the polarity string
                
                # Skip terms with 'conflict' polarity, as done in the paper
                if polarity_str == 'conflict' or polarity_str not in polarity_map:
                    continue
                
                # Map polarity string to integer
                polarity_int = polarity_map[polarity_str]
                
                # The 'from' and 'to' attributes are character offsets
                start = int(aspect_term_elem.get('from'))
                end = int(aspect_term_elem.get('to'))
                
                # Reconstruct the sentence with the $T$ placeholder
                left_part = original_text[:start]
                right_part = original_text[end:]
                sentence_with_placeholder = left_part + "$T$" + right_part
                
                # Write the 3-line entry to the output file
                f_out.write(sentence_with_placeholder.lower().strip() + '\n')
                f_out.write(term.lower().strip() + '\n')
                f_out.write(str(polarity_int) + '\n')
                entry_count += 1

    print(f"Conversion complete.")
    print(f"Processed {entry_count} aspect term entries and saved them to '{output_file}'.")

if __name__ == "__main__":
    # Define input and output filenames
    inputs = ["train", "test"]
    # Process each dataset
    for dataset in inputs:
            input_filename = f"MAMS_{dataset}.xml"
            output_filename = f"MAMS_{dataset}.raw"
            convert_xml(input_filename, output_filename)