"""
simulate_tickets_resale.py

Simulate tickets being added to resale by inserting into Tickets_In_Resale,
triggering the stored procedures and triggers for ticket reassignment or queue management.
"""

import mysql.connector
import random
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database='Festival'
    )

def simulate_resale(num_simulations):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all ticket IDs along with their corresponding Event_ID
    cursor.execute("SELECT ID, Event_ID FROM Ticket")
    tickets = cursor.fetchall()  # This will give a list of tuples (Ticket_ID, Event_ID)

    # Simulate tickets being placed in resale queue
    for i in range(num_simulations):
        ticket_id, event_id = random.choice(tickets)  # Randomly select a ticket and its corresponding event ID
        try:
            # Insert the ticket into the resale queue
            cursor.execute(
                "INSERT INTO Tickets_In_Resale (Ticket_ID, Event_ID) VALUES (%s, %s)",
                (ticket_id, event_id)
            )
            conn.commit()
            print(f"[{i+1}] Ticket {ticket_id} for Event {event_id}: Success")
        except mysql.connector.Error as err:
            print(f"[{i+1}] Ticket {ticket_id} for Event {event_id}: {err.msg}")
            conn.rollback()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simulate tickets being placed in resale queue.')
    parser.add_argument('-n', '--num', type=int, default=1000, help='Number of simulation attempts')
    args = parser.parse_args()
    simulate_resale(args.num)
