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

    # Fetch tickets that:
    # - Belong to a spectator
    # - Are NOT in Tickets_In_Resale
    # - Have NOT already been resold
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

    resale_success_count = 0
    resale_queue_count = 0
    resale_error_count = 0

    for i in range(min(num_simulations, len(tickets))):
        ticket_id, event_id = random.choice(tickets)
        tickets.remove((ticket_id, event_id))  # Prevent duplicate resale

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

            # Check if the ticket was resold immediately via trigger
            cursor.execute(
                "SELECT COUNT(*) FROM Transaction WHERE Ticket_ID = %s AND Is_Resale = TRUE",
                (ticket_id,)
            )
            resale_occurred = cursor.fetchone()[0] > 0

            if resale_occurred:
                cursor.execute(
                    "UPDATE Ticket SET Still_In_Resale = FALSE WHERE ID = %s",
                    (ticket_id,)
                )
                conn.commit()
                print(f"[{i+1}] Ticket {ticket_id} for Event {event_id}: Resold immediately (transaction match)")
                resale_success_count += 1
            else:
                print(f"[{i+1}] Ticket {ticket_id} for Event {event_id}: Added to resale queue")
                resale_queue_count += 1

        except mysql.connector.Error as err:
            print(f"[{i+1}] Ticket {ticket_id} for Event {event_id}: {err.msg}")
            resale_error_count += 1
            conn.rollback()

    print("\n--- Simulation Summary ---")
    print(f"Successful resales (via transaction): {resale_success_count}")
    print(f"Tickets added to resale queue: {resale_queue_count}")
    print(f"Total attempted: {resale_success_count + resale_queue_count + resale_error_count}")
    print(f"Resale errors: {resale_error_count}")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simulate tickets being placed in resale queue.')
    parser.add_argument('-n', '--num', type=int, default=1000, help='Number of simulation attempts')
    args = parser.parse_args()
    simulate_resale(args.num)
