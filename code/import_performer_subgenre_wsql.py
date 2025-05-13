#!/usr/bin/env python3
"""
import_performer_subgenre.py

Generates mappings between performers and subgenres,
inserts them into the Performer_Subgenre table,
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
    'password': '',
    'database': 'festival'
}
SQL_FILENAME = 'generated_performer_subgenre.sql'

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Initialize random seed
epoch_seed = int(datetime.now().timestamp())
random.seed(epoch_seed)

# ---------------- FETCH IDs ----------------
cursor.execute("SELECT ID FROM Performer")
performer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT ID FROM Subgenre")
subgenre_ids = [row[0] for row in cursor.fetchall()]

if not performer_ids or not subgenre_ids:
    print("Missing performers or subgenres in the database.")
    cursor.close()
    conn.close()
    exit()

# ---------------- GENERATE LINKS ----------------
link_rows = set()

for performer_id in performer_ids:
    count = random.randint(1, 3)
    assigned_subgenres = random.sample(subgenre_ids, count)
    for subgenre_id in assigned_subgenres:
        link_rows.add((performer_id, subgenre_id))

# ---------------- INSERT INTO DB ----------------
insert_sql = """
INSERT IGNORE INTO Performer_Subgenre (Performer_ID, Subgenre_ID)
VALUES (%s, %s)
"""

try:
    cursor.executemany(insert_sql, list(link_rows))
    conn.commit()
    print(f"Inserted {cursor.rowcount} performer-subgenre links into the database.")
except mysql.connector.Error as err:
    print(f"Error inserting links: {err}")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Performer_Subgenre table\n')
        for performer_id, subgenre_id in rows:
            f.write(
                f"INSERT IGNORE INTO Performer_Subgenre (Performer_ID, Subgenre_ID) "
                f"VALUES ({performer_id}, {subgenre_id});\n"
            )

# ---------------- CLEAN UP ----------------
cursor.close()
conn.close()
print("Database connection closed.")

# ---------------- MAIN ----------------
def main():
    write_sql_file(link_rows, SQL_FILENAME)

if __name__ == '__main__':
    main()
