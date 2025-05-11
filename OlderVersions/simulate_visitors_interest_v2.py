#!/usr/bin/env python3
"""
simulate_visitors_interest.py

Simulate each visitor expressing interest in a random number of different events by inserting
into Visitor_Interested_Event, triggering the stored procedures and triggers
for ticket assignment or waitlisting.
"""

import mysql.connector
import random
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'xaua6709ni!'),
        database='Festival'
    )

def simulate_interest():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all visitor IDs
    cursor.execute("SELECT ID FROM Visitor")
    visitors = [row[0] for row in cursor.fetchall()]

    # Fetch all event IDs
    cursor.execute("SELECT ID FROM Event")
    events = [row[0] for row in cursor.fetchall()]

    # Fetch all ticket type IDs
    cursor.execute("SELECT Name FROM Type")
    types = [row[0] for row in cursor.fetchall()]

    # Fetch all payment type IDs
    cursor.execute("SELECT Name FROM Payment")
    payments = [row[0] for row in cursor.fetchall()]

    for v in visitors:
        # Choose a random number of distinct events for this visitor
        num_events = random.randint(1, 3)
        chosen_events = random.sample(events, num_events)

        for e in chosen_events:
            t = random.choice(types)
            p = random.choice(payments)
            try:
                # Insert interest with random type and payment
                cursor.execute(
                    "INSERT INTO Visitor_Interested_Event (Event_ID, Visitor_ID, Type_ID, Payment_ID) "
                    "VALUES (%s, %s, %s, %s)",
                    (e, v, t, p)
                )
                conn.commit()
                print(f"Visitor {v} -> Event {e} (Type {t}, Payment {p}): Success")
            except mysql.connector.Error as err:
                print(f"Visitor {v} -> Event {e} (Type {t}, Payment {p}): {err.msg}")
                conn.rollback()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    simulate_interest()
