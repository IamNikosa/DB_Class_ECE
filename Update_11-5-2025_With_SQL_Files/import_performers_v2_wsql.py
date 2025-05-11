#!/usr/bin/env python3
"""
import_performers.py

Generates fake performers and band memberships, inserts into the Performer and Membership
Tables, and writes corresponding INSERT statements into a .sql file in the same directory.
"""
import os
import random
import mysql.connector
from faker import Faker
from datetime import datetime

# ---------------- SETUP ----------------
# Ensure script runs from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xaua6709ni!',  
    'database': 'festival'
}
SQL_FILENAME = 'generated_performers_and_memberships.sql'
NUM_PERFORMERS = 80

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# ---------------- GENERATE DATA ----------------
fake = Faker()
seed_val = int(datetime.now().timestamp())
Faker.seed(seed_val)
random.seed(seed_val)

performers = []
bands = []
solo_artists = []
memberships = []

for i in range(1, NUM_PERFORMERS + 1):
    is_band = random.choice([True, False])
    real_name = fake.name().replace("'", "''") if not is_band else None
    stage_name_raw = fake.word().capitalize() + (" Band" if is_band else " Artist")
    stage_name = stage_name_raw.replace("'", "''")
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=60) if not is_band else None
    formation_date = fake.date_between(start_date='-30y', end_date='-1y') if is_band else None
    instagram = fake.user_name().replace("'", "''")
    website = fake.url().replace("'", "''")

    performers.append(
        (i,
         real_name,
         stage_name,
         birthday,
         instagram,
         website,
         int(is_band),
         formation_date)
    )

    if is_band:
        bands.append(i)
    else:
        solo_artists.append(i)

# Generate memberships: assign some solo artists to bands
for artist_id in solo_artists[:]:
    if bands and random.random() < 0.6:
        band_id = random.choice(bands)
        memberships.append((band_id, artist_id, fake.date_between(start_date='-10y', end_date='today')))
# Ensure each band has at least two members
for band_id in bands:
    members = [m for m in memberships if m[0] == band_id]
    if len(members) < 2 and solo_artists:
        artist_id = solo_artists.pop(0)
        memberships.append((band_id, artist_id, fake.date_between(start_date='-10y', end_date='today')))

# ---------------- INSERT INTO DB ----------------
insert_perf_sql = (
    "INSERT INTO Performer "
    "(ID, Real_Name, Stage_Name, Birthday, Instagram, Website, Is_Band, Formation_Date) VALUES "
    "(%s, %s, %s, %s, %s, %s, %s, %s)"
)
cursor.executemany(insert_perf_sql, performers)
conn.commit()
print(f"Inserted {cursor.rowcount} performers into the database.")

if memberships:
    insert_mem_sql = (
        "INSERT INTO Membership (Band_ID, Artist_ID, Join_Date) VALUES (%s, %s, %s)"
    )
    cursor.executemany(insert_mem_sql, memberships)
    conn.commit()
    print(f"Inserted {cursor.rowcount} membership rows into the database.")

# ---------------- WRITE .SQL FILE ----------------

def write_sql_file(performers, memberships, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Performer table\n')
        for p in performers:
            id_, real, stage, bday, insta, web, isb, form = p
            vals = [
                str(id_),
                f"'{real}'" if real else 'NULL',
                f"'{stage}'",
                f"'{bday}'" if bday else 'NULL',
                f"'{insta}'",
                f"'{web}'",
                str(isb),
                f"'{form}'" if form else 'NULL'
            ]
            f.write(f"INSERT INTO Performer (ID, Real_Name, Stage_Name, Birthday, Instagram, Website, Is_Band, Formation_Date) VALUES ({', '.join(vals)});\n")
        if memberships:
            f.write('\n-- Generated INSERTs for Membership table\n')
            for m in memberships:
                f.write(f"INSERT INTO Membership (Band_ID, Artist_ID, Join_Date) VALUES ({m[0]}, {m[1]}, '{m[2]}');\n")

write_sql_file(performers, memberships, SQL_FILENAME)

# ---------------- CLEANUP ----------------
cursor.close()
conn.close()
print("Database connection closed.")
