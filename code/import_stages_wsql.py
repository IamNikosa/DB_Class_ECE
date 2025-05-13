#!/usr/bin/env python3
import os
import mysql.connector
from faker import Faker
import random

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'festival'
}

NUM_STAGES = 50
SQL_FILENAME = 'generated_stages.sql'

# ---------------- SETUP ----------------
# ensure working dir is script dir
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Connect to the database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# ---------------- CLEAN UP EXISTING DATA ----------------
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DELETE FROM Stage")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Initialize Faker
fake = Faker()
Faker.seed(1)
random.seed(1)

# ---------------- GENERATE STAGE DATA ----------------
stage_rows = []
for stage_id in range(1, NUM_STAGES + 1):
    name        = fake.company() + " Stage"
    description = fake.sentence(nb_words=6).replace("'", "''")
    capacity    = random.randint(100, 200)
    tech_info   = fake.catch_phrase().replace("'", "''")

    stage_rows.append((stage_id, name, description, capacity, tech_info))

# ---------------- INSERT INTO DB ----------------
insert_sql = """
INSERT INTO Stage (ID, Name, Description, Capacity, Tech_Info)
VALUES (%s, %s, %s, %s, %s)
"""
try:
    cursor.executemany(insert_sql, stage_rows)
    conn.commit()
    print(f"{cursor.rowcount} fake stages inserted successfully.")
except mysql.connector.Error as err:
    conn.rollback()
    print(f"Database error: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")

# ---------------- DUMP TO .SQL FILE ----------------
with open(SQL_FILENAME, 'w', encoding='utf-8') as f:
    f.write(f'-- Generated INSERTs for Stage table ({NUM_STAGES} rows)\n')
    for row in stage_rows:
        sid, nm, desc, cap, tech = row
        stmt = (
            "INSERT INTO Stage (ID, Name, Description, Capacity, Tech_Info) VALUES "
            f"({sid}, '{nm}', '{desc}', {cap}, '{tech}');\n"
        )
        f.write(stmt)

