#!/usr/bin/env python3
"""
simulate_visitor_interest.py

Simulates visitors expressing interest in random events by inserting into Visitor_Interested_Event,
triggering any procedures or triggers for ticket assignment or waitlisting.
Writes all successful inserts to a .sql file.
"""

import mysql.connector
import random
import os
from datetime import datetime

# ---------------- SETUP ----------------
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': 'Festival'
}
SQL_FILENAME = 'generated_visitors_interest.sql'

# ---------------- CONNECT ----------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- SIMULATION ----------------
def simulate_interest(num_simulations=100):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch required IDs
    cursor.execute("SELECT ID FROM Visitor")
    visitors = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT ID FROM Event")
    events = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Name FROM Type")
    types = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Name FROM Payment")
    payments = [row[0] for row in cursor.fetchall()]

    if not visitors or not events or not types or not payments:
        print("One or more necessary tables are empty.")
        cursor.close()
        conn.close()
        return []

    inserts = []
    visited_pairs = set()
    success_count = 0

    for i in range(num_simulations):
        v = random.choice(visitors)
        e = random.choice(events)

        if (v, e) in visited_pairs:
            continue

        t = random.choice(types)
        p = random.choice(payments)

        try:
            cursor.execute("""
                INSERT INTO Visitor_Interested_Event (Event_ID, Visitor_ID, Type_ID, Payment_ID)
                VALUES (%s, %s, %s, %s)
            """, (e, v, t, p))
            conn.commit()

            visited_pairs.add((v, e))
            inserts.append((e, v, t, p))
            success_count += 1

            #print(f"[{success_count}] Visitor {v} -> Event {e} (Type {t}, Payment {p}): Success")

        except mysql.connector.Error as err:
            #print(f"[{i+1}] Visitor {v} -> Event {e} (Type {t}, Payment {p}): {err.msg}")
            conn.rollback()

    cursor.close()
    conn.close()
    print(f"\nInserted {success_count} interest records.")
    return inserts

# ---------------- WRITE SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Visitor_Interested_Event\n')
        for e, v, t, p in rows:
            f.write(
                f"INSERT INTO Visitor_Interested_Event (Event_ID, Visitor_ID, Type_ID, Payment_ID) "
                f"VALUES ({e}, {v}, '{t}', '{p}');\n"
            )

# ---------------- MAIN ----------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Simulate visitor interest in events.')
    parser.add_argument('-n', '--num', type=int, default=10000, help='Number of simulation attempts')
    args = parser.parse_args()

    inserted = simulate_interest(args.num)
    if inserted:
        write_sql_file(inserted, SQL_FILENAME)

if __name__ == '__main__':
    main()
