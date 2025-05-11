#!/usr/bin/env python3
"""
import_genres.py

Inserts predefined genres into the Genre table,
and writes corresponding INSERT statements to a .sql file
in the same directory as this script.
"""
import os
import random
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
    'password': 'xaua6709ni!',
    'database': 'Festival'
}
SQL_FILENAME = 'generated_genres.sql'

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# ---------------- GENRE SETUP ----------------
genre_names = [
    'Rock', 'Jazz', 'Classical', 'Hip Hop', 'Electronic', 'Pop',
    'Folk', 'Blues', 'Reggae', 'Metal', 'Punk', 'Country',
    'Soul', 'Funk', 'Techno', 'Opera', 'R&B', 'Indie', 'House', 'Trance'
]

# Remove duplicates already in table
cursor.execute("SELECT Name FROM Genre")
existing = {row[0] for row in cursor.fetchall()}
new_genres = [g for g in genre_names if g not in existing]

# Determine starting ID
cursor.execute("SELECT MAX(ID) FROM Genre")
row = cursor.fetchone()
start_id = (row[0] or 0) + 1

# Build genre data
genre_rows = [(start_id + i, name) for i, name in enumerate(new_genres)]

# ---------------- INSERT INTO DB ----------------
insert_sql = "INSERT INTO Genre (ID, Name) VALUES (%s, %s)"

try:
    cursor.executemany(insert_sql, genre_rows)
    conn.commit()
    print(f"Inserted {cursor.rowcount} genres into the database.")
except mysql.connector.Error as err:
    print(f"Error inserting genres: {err}")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Genre table\n')
        for gid, name in rows:
            name_escaped = name.replace("'", "''")
            f.write(f"INSERT INTO Genre (ID, Name) VALUES ({gid}, '{name_escaped}');\n")

# Clean up DB connections
cursor.close()
conn.close()
print("Database connection closed.")

# Finally write to .sql file
def main():
    write_sql_file(genre_rows, SQL_FILENAME)

if __name__ == '__main__':
    main()
