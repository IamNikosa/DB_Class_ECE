#!/usr/bin/env python3
"""
import_events.py

Generates fake events, inserts them into the Event table,
and writes corresponding INSERT statements to a .sql file
in the same directory as this script.
"""
import os
import random
import mysql.connector
from faker import Faker
from datetime import datetime, timedelta

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
SQL_FILENAME = 'generated_events.sql'
NUM_EVENTS = 80

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Initialize Faker and random seed
epoch_seed = int(datetime.now().timestamp())
fake = Faker()
Faker.seed(epoch_seed)
random.seed(epoch_seed)

# ---------------- FETCH REFS ----------------n# Retrieve existing Stage and Festival data to reference
cursor.execute("SELECT ID FROM Stage ORDER BY ID")
stage_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT ID, Start_Date FROM Festival ORDER BY ID")
festival_rows = cursor.fetchall()
# Convert start_date to datetime
festival_data = [(fid, datetime.combine(sdate, datetime.min.time())) for fid, sdate in festival_rows]

if not stage_ids or not festival_data:
    raise RuntimeError("Stage and Festival tables must have data before generating events.")

# ---------------- GENERATE EVENTS ----------------
event_rows = []
used_combinations = set()
for event_id in range(1, NUM_EVENTS + 1):
    attempts = 0
    while attempts < 10:
        fest_id, fest_start = random.choice(festival_data)
        stage_id = random.choice(stage_ids)
        # pick start_time within 7 days of festival
        start_dt = fake.date_time_between(start_date=fest_start, end_date=fest_start + timedelta(days=6))
        end_dt = start_dt + timedelta(hours=random.randint(1, 4))
        combo_key = (fest_id, stage_id, start_dt)
        if combo_key not in used_combinations:
            used_combinations.add(combo_key)
            sold_out = False
            event_rows.append((event_id, start_dt, end_dt, sold_out, fest_id, stage_id))
            break
        attempts += 1

# ---------------- INSERT INTO DB ----------------
insert_sql = (
    "INSERT INTO Event (ID, Start_Time, End_Time, Sold_Out, Festival_ID, Stage_ID) "
    "VALUES (%s, %s, %s, %s, %s, %s)"
)
cursor.executemany(insert_sql, event_rows)
conn.commit()
print(f"Inserted {cursor.rowcount} events into the database.")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Event table\n')
        for row in rows:
            eid, st, et, sold, fid, sid = row
            sold_int = 1 if sold else 0
            st_str = st.strftime('%Y-%m-%d %H:%M:%S')
            et_str = et.strftime('%Y-%m-%d %H:%M:%S')
            stmt = (
                f"INSERT INTO Event (ID, Start_Time, End_Time, Sold_Out, Festival_ID, Stage_ID) "
                f"VALUES ({eid}, '{st_str}', '{et_str}', {sold_int}, {fid}, {sid});\n"
            )
            f.write(stmt)

# Clean up DB connections
cursor.close()
conn.close()
print("Database connection closed.")

# Finally write to .sql file
def main():
    write_sql_file(event_rows, SQL_FILENAME)

if __name__ == '__main__':
    main()
