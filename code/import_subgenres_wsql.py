#!/usr/bin/env python3
"""
import_subgenres.py

Generates subgenres, inserts them into the Subgenre table,
and writes corresponding INSERT statements to a .sql file
in the same directory as this script.
"""
import os
import random
from faker import Faker
import mysql.connector
from datetime import datetime

# ---------------- SETUP ----------------
# Ensure script runs from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Festival'
}
SQL_FILENAME = 'generated_subgenres.sql'
NUM_SUBGENRES = 20

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Initialize Faker
epoch_seed = int(datetime.now().timestamp())
fake = Faker()
Faker.seed(epoch_seed)
random.seed(epoch_seed)

# ---------------- FETCH GENRE IDs ----------------
cursor.execute("SELECT ID FROM Genre")
genre_ids = [row[0] for row in cursor.fetchall()]
if not genre_ids:
    raise RuntimeError("No genres found — cannot assign subgenres.")

# ---------------- BUILD SUBGENRE NAMES ----------------
cursor.execute("SELECT Name FROM Subgenre")
existing_subgenre_names = {row[0] for row in cursor.fetchall()}

base_names = [
    'Synthpop', 'Death Metal', 'Smooth Jazz', 'Trap', 'Indie Rock',
    'Electro Swing', 'Boom Bap', 'Grime', 'Neo Soul', 'Dub',
    'Tech House', 'Ska Punk', 'Drum and Bass', 'Tango Nuevo',
    'Opera Buffa', 'Post-Rock', 'Shoegaze', 'Trip Hop', 'Bossa Nova',
    'Glitch Hop', 'Vaporwave', 'Chillwave', 'Black Metal', 'Space Jazz'
]

used_names = existing_subgenre_names.copy()
subgenre_names = []

while len(subgenre_names) < NUM_SUBGENRES:
    if base_names:
        name = base_names.pop(0)
    else:
        name = fake.unique.word().title() + " " + random.choice(["Style", "Wave", "Core", "Beats"])
    if name not in used_names:
        subgenre_names.append(name)
        used_names.add(name)

# ---------------- GENERATE SUBGENRE DATA ----------------
cursor.execute("SELECT MAX(ID) FROM Subgenre")
row = cursor.fetchone()
start_id = row[0] + 1 if row[0] is not None else 1

subgenre_rows = [
    (start_id + i, name, random.choice(genre_ids))
    for i, name in enumerate(subgenre_names)
]

# ---------------- INSERT INTO DB ----------------
insert_sql = "INSERT INTO Subgenre (ID, Name, Genre_ID) VALUES (%s, %s, %s)"
try:
    cursor.executemany(insert_sql, subgenre_rows)
    conn.commit()
    print(f"Inserted {cursor.rowcount} subgenres into the database.")
except mysql.connector.Error as err:
    print(f"Error inserting subgenres: {err}")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Subgenre table\n')
        for sid, name, gid in rows:
            name_escaped = name.replace("'", "''")
            f.write(f"INSERT INTO Subgenre (ID, Name, Genre_ID) VALUES ({sid}, '{name_escaped}', {gid});\n")

# ---------------- CLEAN UP ----------------
cursor.close()
conn.close()
print("Database connection closed.")

# ---------------- MAIN ----------------
def main():
    write_sql_file(subgenre_rows, SQL_FILENAME)

if __name__ == '__main__':
    main()
