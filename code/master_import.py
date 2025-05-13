#!/usr/bin/env python3
import subprocess
import os
import sys

# Ensure working directory is the script's own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Master import script to execute individual data loaders in correct dependency order
scripts = [
    # foundational lookups
    "import_locations_wsql.py",        # Location
    "import_stages_wsql.py",           # Stage
    "import_payment-ticket_type_wsql.py",   # Payment, Type

    # core entities
    "import_festivals_v2_wsql.py",           # Festival ← Location
    "import_performers_v2_wsql.py",            # Performer
    "import_events_v2_wsql.py",                # Event ← Festival, Stage

    # ticketing & people
    "import_visitors_wsql.py",              # Visitor
    "import_tickets_v2_wsql.py",               # Ticket ← Event, Type, Payment

    # performances & reviews
    "import_performances_v2_wsql.py",          # Performance ← Event, Performer
    "import_genres_wsql.py",                # Genre
    "import_subgenres_wsql.py",             # Subgenre ← Genre
    "import_performer_subgenre_wsql.py",    # Performer↔Subgenre

    # staff assignments & images
    "import_staff_event_staff_v2_wsql.py",     # Staff & event_staff
    "import_images_of_everything_wsql.py",     # Image + *_image join tables

    # simulations
    "simulate_visitors_interest_v3_wsql.py", 
    "simulate_tickets_in_resale_v3_wsql.py",

    # Reviews
    "import_reviews_v3_wsql.py",               # Review ← Ticket
]

if __name__ == '__main__':
    for script in scripts:
        print(f"\n=== Running {script} ===")
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True
        )
        # Print stdout
        if result.stdout:
            print(result.stdout)
        # If error, print stderr and exit
        if result.returncode != 0:
            print(f"Error: {script} exited with code {result.returncode}", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)
            
