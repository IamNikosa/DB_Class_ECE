#!/usr/bin/env python3
import mysql.connector
import random
import sys
from datetime import timedelta

# ——— DB setup ———
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Fest"
)
cursor = conn.cursor()

random.seed(42)

# ——— Load events and performers ———
cursor.execute("SELECT ID, Start_Time, End_Time FROM Event")
events = cursor.fetchall()  # [(event_id, datetime), …]

cursor.execute("SELECT ID FROM Performer")
performers = [r[0] for r in cursor.fetchall()]
if not events or not performers:
    print("No events or no performers found – aborting.")
    sys.exit(1)

# ——— Prepare for inserts ———
insert_sql = """
INSERT INTO Performance
  (ID, Type, Start_Time, Duration, Performer_ID, Event_ID)
VALUES (%s, %s, %s, %s, %s, %s)
"""
TYPES = ['Warm up', 'Head line', 'Special guest']

perf_id = 1
inserted = skipped = 0

for event_id, event_start, event_end in events:
    current_start = event_start

    # pick up to 5 random artists
    selected = random.sample(performers, min(5, len(performers)))

    for artist in selected:
        duration = random.randint(10, 50)
        gap      = random.randint(5, 30)            # guaranteed within trigger window

        start_dt = current_start
        end_dt   = start_dt + timedelta(minutes=duration)

        if end_dt > event_end:
            # print(f"Event {event_id}: can't fit a {duration}m slot starting at {start_dt.time()}, stopping.")
            break

        params = (
            perf_id,
            random.choice(TYPES),
            start_dt.time(),    # TIME column
            duration,
            artist,
            event_id
        )
        try:
            cursor.execute(insert_sql, params)
            conn.commit()
            inserted += 1

            # record in-memory
            perf_id += 1

            # advance for next slot
            current_start = end_dt + timedelta(minutes=gap)

        except mysql.connector.Error as err:
            # unexpected error: log & rollback
            # print(f" Skipped perf#{perf_id} (evt={event_id}, art={artist}): {err.msg}")
            conn.rollback()
            skipped += 1

# print(f"\nInserted {inserted} performances. Skipped {skipped} due to overlaps.")
print(f"\nInserted {inserted} performances")
cursor.close()
conn.close()
