import os
# Detect the folder where this script is stored
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ordered list of .sql filenames (these must exist in the same directory as this script)
ordered_files = [
    "generated_locations.sql",
    "generated_stages.sql",
    "generated_payment_and_types.sql",
    
    "generated_festivals.sql",
    "generated_performers_and_memberships.sql",
    "generated_events.sql",
    
    "generated_visitors.sql",
    "generated_tickets.sql",
    
    "generated_performances.sql",
    "generated_genres.sql",
    "generated_subgenres.sql",
    "generated_performer_subgenre.sql",
    
    "generated_event_staff.sql",
    "generated_images.sql",
    
    "generated_visitors_interest.sql",
    "generated_resale_tickets.sql",
    
    "generated_reviews.sql"
]


output_path = os.path.join(script_dir, "load.sql")

with open(output_path, 'w', encoding='utf-8') as outfile:
    for filename in ordered_files:
        file_path = os.path.join(script_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(f"-- FILE: {filename}\n")
                outfile.write(infile.read())
                outfile.write("\n\n")
        else:
            print(f"[WARNING] File not found: {filename}")

print(f"\nCombined .sql written to: {output_path}")
