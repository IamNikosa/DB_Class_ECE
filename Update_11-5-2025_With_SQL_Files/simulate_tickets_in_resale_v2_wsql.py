#!/usr/bin/env python3
"""
simulate_tickets_resale.py

Simulates tickets being added to resale by inserting into Tickets_In_Resale,
triggering stored procedures for reassignment or queue management.
Writes executed resale inserts to a .sql file.
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
SQL_FILENAME = 'generated_resale_tickets.sql'

# ---------------- CONNECT ----------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- SIMULATION ----------------
def simulate_resale(num_simulations):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Select eligible tickets
    cursor.execute("""
        SELECT ID, Event_ID 
        FROM Ticket 
        WHERE ID IN (SELECT Ticket_ID FROM Spectator)
          AND ID NOT IN (SELECT Ticket_ID FROM Tickets_In_Resale)
          AND ID NOT IN (
              SELECT Ticket_ID FROM Transaction WHERE Is_Resale = TRUE
          )
    """)
    tickets = cursor.fetchall()

    if not tickets:
        print("No eligible tickets found.")
        cursor.close()
        conn.close()
        return []

    inserts = []
    success = queue = error = 0

    for i in range(min(num_simulations, len(tickets))):
        ticket_id, event_id = random.choice(tickets)
        tickets.remove((ticket_id, event_id))

        try:
            cursor.execute(
                "INSERT INTO Tickets_In_Resale (Ticket_ID, Event_ID) VALUES (%s, %s)",
                (ticket_id, event_id)
            )
            cursor.execute(
                "UPDATE Ticket SET Still_In_Resale = TRUE WHERE ID = %s",
                (ticket_id,)
            )
            conn.commit()

            # Check if immediately resold
            cursor.execute("""
                SELECT COUNT(*) FROM Transaction 
                WHERE Ticket_ID = %s AND Is_Resale = TRUE
            """, (ticket_id,))
            resold = cursor.fetchone()[0] > 0

            if resold:
                cursor.execute(
                    "UPDATE Ticket SET Still_In_Resale = FALSE WHERE ID = %s",
                    (ticket_id,)
                )
                conn.commit()
                print(f"[{i+1}] Ticket {ticket_id} → Event {event_id}: Resold immediately.")
                success += 1
            else:
                print(f"[{i+1}] Ticket {ticket_id} → Event {event_id}: Added to resale queue.")
                queue += 1

            inserts.append((ticket_id, event_id))

        except mysql.connector.Error as err:
            print(f"[{i+1}] Ticket {ticket_id} → Event {event_id}: {err.msg}")
            conn.rollback()
            error += 1

    print("\n--- Simulation Summary ---")
    print(f"Resold immediately: {success}")
    print(f"In resale queue: {queue}")
    print(f"Errors: {error}")
    print(f"Total attempted: {success + queue + error}")

    cursor.close()
    conn.close()
    return inserts

# ---------------- WRITE SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Resale ticket inserts\n')
        for ticket_id, event_id in rows:
            f.write(
                f"INSERT INTO Tickets_In_Resale (Ticket_ID, Event_ID) VALUES ({ticket_id}, {event_id});\n"
            )

# ---------------- MAIN ----------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Simulate tickets entering resale queue.')
    parser.add_argument('-n', '--num', type=int, default=1000, help='Number of simulation attempts')
    args = parser.parse_args()

    inserted = simulate_resale(args.num)
    if inserted:
        write_sql_file(inserted, SQL_FILENAME)

if __name__ == '__main__':
    main()
