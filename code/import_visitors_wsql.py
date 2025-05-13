#!/usr/bin/env python3
"""
import_visitors.py

Generates fake visitor entries, inserts them into the Visitor table,
and writes corresponding INSERT statements to a .sql file
in the same directory as this script.
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
    'password': '',  
    'database': 'Festival'
}
SQL_FILENAME = 'generated_visitors.sql'
NUM_VISITORS = 2000

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Initialize Faker and random seed
epoch_seed = int(datetime.now().timestamp())
fake = Faker()
Faker.seed(epoch_seed)
random.seed(epoch_seed)

# ---------------- GENERATE VISITORS ----------------
visitor_rows = []

for visitor_id in range(1, NUM_VISITORS + 1):
    first_name = fake.first_name().replace("'", "''")
    last_name = fake.last_name().replace("'", "''")
    age = random.randint(16, 70)
    con_info = fake.email().replace("'", "''")
    visitor_rows.append((visitor_id, first_name, last_name, age, con_info))

# ---------------- INSERT INTO DB ----------------
insert_sql = (
    "INSERT INTO Visitor (ID, First_Name, Last_Name, Age, Con_Info) "
    "VALUES (%s, %s, %s, %s, %s)"
)
cursor.executemany(insert_sql, visitor_rows)
conn.commit()
print(f"Inserted {cursor.rowcount} visitors into the database.")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Visitor table\n')
        for row in rows:
            visitor_id, first, last, age, email = row
            stmt = (
                f"INSERT INTO Visitor (ID, First_Name, Last_Name, Age, Con_Info) "
                f"VALUES ({visitor_id}, '{first}', '{last}', {age}, '{email}');\n"
            )
            f.write(stmt)

# Clean up DB connections
cursor.close()
conn.close()
print("Database connection closed.")

# Finally write to .sql file
def main():
    write_sql_file(visitor_rows, SQL_FILENAME)

if __name__ == '__main__':
    main()
