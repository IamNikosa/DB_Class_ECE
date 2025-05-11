import mysql.connector
import random
import sys
from datetime import timedelta

# ——— DB setup ———
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="festival"
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

# Step 1: Pick one random performer
persistent_performer = random.choice(performers)

# Step 2: Organize events by year
from collections import defaultdict
events_by_year = defaultdict(list)
for event_id, start, end in events:
    events_by_year[start.year].append((event_id, start, end))

# Step 3: Insert at least one performance per year for the selected performer
for year, year_events in events_by_year.items():
    random_event = random.choice(year_events)
    event_id, event_start, event_end = random_event

    duration = random.randint(10, 50)
    gap = random.randint(5, 30)
    start_dt = event_start
    end_dt = start_dt + timedelta(minutes=duration)

    if end_dt <= event_end:
        performance_type = 'Warm up' if random.random() < 0.5 else random.choice(['Head line', 'Special guest'])
        params = (
            perf_id,
            performance_type,
            start_dt.time(),
            duration,
            persistent_performer,
            event_id
        )
        try:
            cursor.execute(insert_sql, params)
            conn.commit()
            inserted += 1
            perf_id += 1
        except mysql.connector.Error as err:
            conn.rollback()
            skipped += 1

for event_id, event_start, event_end in events:
    current_start = event_start

    # pick up to 8 random artists
    selected = random.sample(performers, min(8, len(performers)))

    for artist in selected:
        duration = random.randint(10, 50)
        gap      = random.randint(5, 30)  # guaranteed within trigger window

        start_dt = current_start
        end_dt   = start_dt + timedelta(minutes=duration)

        if end_dt > event_end:
            break

        # Randomly choose performance type with 50% chance for "Warm up"
        performance_type = 'Warm up' if random.random() < 0.7 else random.choice(['Head line', 'Special guest'])

        params = (
            perf_id,
            performance_type,
            start_dt.time(),  # TIME column
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
            conn.rollback()
            skipped += 1

print(f"\nInserted {inserted} performances.")
print(f"Skipped {skipped} due to overlaps.")

cursor.close()
conn.close()
