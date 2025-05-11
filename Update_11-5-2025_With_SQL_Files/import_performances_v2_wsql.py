#!/usr/bin/env python3
"""
import_performances.py

Generates fake performance entries, inserts them into the Performance table,
and writes corresponding INSERT statements to a .sql file
in the same directory as this script.
"""
import os
import sys
import random
from datetime import datetime, timedelta
from collections import defaultdict
import mysql.connector

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
SQL_FILENAME = 'generated_performances.sql'

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Initialize random seed
epoch_seed = int(datetime.now().timestamp())
random.seed(epoch_seed)

# ---------------- FETCH EVENTS & PERFORMERS ----------------
cursor.execute("SELECT ID, Start_Time, End_Time FROM Event")
events = cursor.fetchall()

cursor.execute("SELECT ID FROM Performer")
performers = [row[0] for row in cursor.fetchall()]

if not events or not performers:
    print("No events or performers found — aborting.")
    cursor.close()
    conn.close()
    sys.exit(1)

# ---------------- PERFORMANCE GENERATION ----------------
insert_sql = """
INSERT INTO Performance (ID, Type, Start_Time, Duration, Performer_ID, Event_ID)
VALUES (%s, %s, %s, %s, %s, %s)
"""
TYPES = ['Warm up', 'Head line', 'Special guest']
performance_rows = []

perf_id = 1
inserted = skipped = 0

# Step 1: Ensure at least one performance per year for one artist
persistent_performer = random.choice(performers)
events_by_year = defaultdict(list)

for event_id, start_dt, end_dt in events:
    events_by_year[start_dt.year].append((event_id, start_dt, end_dt))

for year, year_events in events_by_year.items():
    event_id, event_start, event_end = random.choice(year_events)
    duration = random.randint(10, 50)
    start_dt = event_start
    end_dt = start_dt + timedelta(minutes=duration)
    if end_dt <= event_end:
        perf_type = 'Warm up' if random.random() < 0.5 else random.choice(TYPES[1:])
        row = (perf_id, perf_type, start_dt.time(), duration, persistent_performer, event_id)
        try:
            cursor.execute(insert_sql, row)
            conn.commit()
            performance_rows.append(row)
            perf_id += 1
            inserted += 1
        except mysql.connector.Error:
            conn.rollback()
            skipped += 1

# Step 2: Fill additional performances
for event_id, event_start, event_end in events:
    current_start = event_start
    selected_artists = random.sample(performers, min(8, len(performers)))

    for artist in selected_artists:
        duration = random.randint(10, 50)
        gap = random.randint(5, 30)
        start_dt = current_start
        end_dt = start_dt + timedelta(minutes=duration)

        if end_dt > event_end:
            break

        perf_type = 'Warm up' if random.random() < 0.7 else random.choice(TYPES[1:])
        row = (perf_id, perf_type, start_dt.time(), duration, artist, event_id)

        try:
            cursor.execute(insert_sql, row)
            conn.commit()
            performance_rows.append(row)
            perf_id += 1
            inserted += 1
            current_start = end_dt + timedelta(minutes=gap)
        except mysql.connector.Error:
            conn.rollback()
            skipped += 1

print(f"\nInserted {inserted} performances.")
print(f"Skipped {skipped} due to overlaps or DB errors.")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Performance table\n')
        for row in rows:
            pid, ptype, stime, duration, perf_id, event_id = row
            f.write(
                f"INSERT INTO Performance (ID, Type, Start_Time, Duration, Performer_ID, Event_ID) "
                f"VALUES ({pid}, '{ptype}', '{stime}', {duration}, {perf_id}, {event_id});\n"
            )

# Clean up DB connections
cursor.close()
conn.close()
print("Database connection closed.")

# Finally write to .sql file
def main():
    write_sql_file(performance_rows, SQL_FILENAME)

if __name__ == '__main__':
    main()
