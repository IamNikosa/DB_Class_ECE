#!/usr/bin/env python3
"""
import_festivals.py

Generates fake festival entries, inserts into the Festival table,
and writes the corresponding INSERT statements to a .sql file
in the same directory as this script.
"""
import os
import random
import mysql.connector
from faker import Faker
import datetime

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
SQL_FILENAME = 'generated_festivals.sql'

# ---------------- CLEAN UP EXISTING DATA ----------------
# Connect to the database
conn = mysql.connector.connect(**DB_CONFIG)
conn.autocommit = True
cursor = conn.cursor()

# Disable foreign-key checks to avoid constraint errors
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
# Delete existing festivals
cursor.execute("DELETE FROM Festival")
# Re-enable foreign-key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# ---------------- INITIALIZE ----------------
fake = Faker()
# seed for reproducibility
seed_val = int(datetime.datetime.now().timestamp())
Faker.seed(seed_val)
random.seed(seed_val)

# Fetch location IDs to assign
cursor.execute("SELECT ID FROM Location ORDER BY ID")
locations = [row[0] for row in cursor.fetchall()]
if not locations:
    raise RuntimeError("No locations in database. Insert locations first.")

# ---------------- GENERATE FESTIVAL DATA ----------------
NUM_FESTIVALS = min(10, len(locations))
festival_values = []
for i in range(NUM_FESTIVALS):
    name = fake.word().capitalize() + " Festival"
    year = 2018 + i
    start_date = fake.date_between(start_date=datetime.date(year, 6, 1),
                                    end_date=datetime.date(year, 9, 1))
    end_date = fake.date_between(start_date=start_date,
                                  end_date=datetime.date(year, 9, 30))
    location_id = locations[i]
    festival_values.append((name, start_date, end_date, location_id))

# Build SQL for insertion
festival_sql = ("INSERT INTO Festival (Name, Start_Date, End_Date, Location_ID) VALUES\n" +
                ",\n".join(
                    f"('{fv[0]}', '{fv[1]}', '{fv[2]}', {fv[3]})"
                    for fv in festival_values
                ) + ";")

# ---------------- INSERT INTO DB ----------------
try:
    cursor.execute(festival_sql)
    print(f"Inserted {NUM_FESTIVALS} festivals into the database.")
except mysql.connector.Error as err:
    print(f"Error inserting festival data: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(sql_text, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERT statements for Festival table\n')
        f.write(sql_text + '\n')

write_sql_file(festival_sql, SQL_FILENAME)
