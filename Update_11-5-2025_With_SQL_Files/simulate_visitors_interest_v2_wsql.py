#!/usr/bin/env python3
"""
simulate_visitors_interest.py

Simulates each visitor expressing interest in 1–3 random events,
inserting into Visitor_Interested_Event and triggering related stored procedures.
Writes corresponding INSERT statements to a .sql file.
"""
import os
import random
import mysql.connector
from datetime import datetime

# ---------------- SETUP ----------------
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'xaua6709ni!'),
    'database': 'Festival'
}
SQL_FILENAME = 'generated_visitors_interest.sql'

# ---------------- CONNECT ----------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- SIMULATION ----------------
def simulate_interest():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all IDs
    cursor.execute("SELECT ID FROM Visitor")
    visitors = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT ID FROM Event")
    events = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Name FROM Type")
    types = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Name FROM Payment")
    payments = [row[0] for row in cursor.fetchall()]

    interest_inserts = []

    for visitor_id in visitors:
        num_events = random.randint(1, 3)
        chosen_events = random.sample(events, num_events)

        for event_id in chosen_events:
            type_id = random.choice(types)
            payment_id = random.choice(payments)
            try:
                cursor.execute("""
                    INSERT INTO Visitor_Interested_Event (Event_ID, Visitor_ID, Type_ID, Payment_ID)
                    VALUES (%s, %s, %s, %s)
                """, (event_id, visitor_id, type_id, payment_id))
                conn.commit()
                interest_inserts.append((event_id, visitor_id, type_id, payment_id))
                #print(f"Visitor {visitor_id} -> Event {event_id} (Type {type_id}, Payment {payment_id}): Success")
            except mysql.connector.Error as err:
                conn.rollback()
                #print(f"Visitor {visitor_id} -> Event {event_id} (Type {type_id}, Payment {payment_id}): {err.msg}")

    cursor.close()
    conn.close()
    print("Simulation completed.")
    return interest_inserts

# ---------------- WRITE SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- INSERTs for Visitor_Interested_Event\n')
        for e_id, v_id, t_id, p_id in rows:
            f.write(
                f"INSERT INTO Visitor_Interested_Event (Event_ID, Visitor_ID, Type_ID, Payment_ID) "
                f"VALUES ({e_id}, {v_id}, '{t_id}', '{p_id}');\n"
            )

# ---------------- MAIN ----------------
def main():
    inserts = simulate_interest()
    write_sql_file(inserts, SQL_FILENAME)

if __name__ == '__main__':
    main()
