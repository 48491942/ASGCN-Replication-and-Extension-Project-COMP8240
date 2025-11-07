# Scrape Reddit Threads and Save Comments to CSV Files
# Import necessary libraries
import praw # PRAW is the Python Reddit API Wrapper
import pandas as pd
import os
import sys

# --- Reddit API Credentials ---
try:
    # Initialize PRAW with Reddit app credentials
    # The user agent is a unique string that identifies the application
    reddit = praw.Reddit(
        # Actual credentials are not included for security reasons
        client_id='client_id', # Replace with client id
        client_secret='client_secret', # Replace with client secret
        user_agent='user_agent'  # Replace with user agent
    )
    # Test credentials
    reddit.user.me()
except Exception as e:
    # Handle authentication errors
    print(f"Error: Could not authenticate with PRAW. Check your credentials. \nDetails: {e}")
    sys.exit(1)


# --- 1. URLs to Scrape ---
# Using a dictionary to map a clean name to each URL.
# This clean name will be used for the output filename.
# Format: 'output_filename_prefix': 'url_to_thread'

threads_to_scrape = {
    'smartphones_positive': "https://www.reddit.com/r/Smartphones/comments/1kew6so/what_is_your_preferred_phone_brand_and_why/",
    'smartphones_negative': "https://www.reddit.com/r/Smartphones/comments/1lsqjmg/what_was_the_worst_smartphone_youve_owned/",
    'laptops_positive': "https://www.reddit.com/r/laptops/comments/1nesjx4/what_laptop_brands_are_the_most_reliable/",
    'laptops_negative': "https://www.reddit.com/r/GamingLaptops/comments/1mt7pj2/whats_the_worst_experience_youve_ever_had_with_a/",
    'fashion_positive': "https://www.reddit.com/r/malefashionadvice/comments/1iy5a0z/best_brands_for_high_quality_well_made_basics/",
    'fashion_negative': "https://www.reddit.com/r/AskReddit/comments/10i8bzk/where_would_you_go_to_find_the_worst_fashion/",
    'restaurants_sydney_positive': "https://www.reddit.com/r/sydney/comments/w6fy67/restaurant_recommendations/",
    'restaurants_sydney_negative': "https://www.reddit.com/r/foodies_sydney/comments/1bcson9/what_restaurants_in_sydney_do_you_think_are/"
}

# --- 2. Output Directory ---
# Check and define the name of the output directory
output_dir = "raw_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Starting to scrape {len(threads_to_scrape)} Reddit threads...")
print("---")

# --- 3. Loop Through Each URL and Scrape ---
# For each thread, fetch comments and save them to a uniquely named CSV file
for file_prefix, url in threads_to_scrape.items():
    try:
        # Fetch the submission using its URL
        print(f"Fetching comments from: {url}")
        submission = reddit.submission(url=url)

        # Create a list to hold comment data
        comments_list = []

        # Load all comments, including nested ones
        submission.comments.replace_more(limit=None)

        # Loop through all top-level comments in the thread
        for comment in submission.comments.list():
            # Append comment text to the list
            comments_list.append({'comment_text': comment.body})

        # Create a DataFrame
        df = pd.DataFrame(comments_list)
        
        # --- 4. Dynamically create the output filename ---
        # The file will be saved inside the 'raw_data' folder
        output_filename = os.path.join(output_dir, f"{file_prefix}_raw.csv")
        
        # Save to the unique CSV file
        df.to_csv(output_filename, index=False)

        print(f"Successfully scraped {len(df)} comments.")
        print(f"Saved to '{output_filename}'")
        print("---")

    except Exception as e:
        # Handle any errors during scraping
        print(f"Error scraping {url}: {e}")
        print("---")

print("All scraping tasks complete.")