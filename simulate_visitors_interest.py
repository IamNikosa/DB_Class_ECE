#!/usr/bin/env python3
"""
simulate_visitors_interest.py

Simulate visitors randomly expressing interest in events by inserting
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

def simulate_interest(num_simulations=100):
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

    for i in range(num_simulations):
        v = random.choice(visitors)
        e = random.choice(events)
        t = random.choice(types)
        p = random.choice(payments)
        try:
            # Correct column order: Event_ID, Visitor_ID, Type_ID, Payment_ID
            cursor.execute(
                "INSERT INTO Visitor_Interested_Event (Event_ID, Visitor_ID, Type_ID, Payment_ID) VALUES (%s, %s, %s, %s)",
                (e, v, t, p)
            )
            conn.commit()
            print(f"[{i+1}] Visitor {v} -> Event {e} (Type {t}, Payment {p}): Success")
        except mysql.connector.Error as err:
            print(f"[{i+1}] Visitor {v} -> Event {e} (Type {t}, Payment {p}): {err.msg}")
            conn.rollback()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simulate visitor interest in events.')
    parser.add_argument('-n', '--num', type=int, default=20000, help='Number of simulation attempts')
    args = parser.parse_args()
    simulate_interest(args.num)
