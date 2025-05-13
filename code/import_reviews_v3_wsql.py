#!/usr/bin/env python3
"""
simulate_reviews.py

Activates tickets for past events and simulates reviews
for ~50% of them. Inserts data into the Ticket and Review tables,
and writes corresponding INSERT statements to a .sql file.
"""
import os
import random
import mysql.connector
from datetime import datetime

# ---------------- SETUP ----------------
# Ensure script runs from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Festival'
}
ACTIVATION_PROBABILITY = 0.95
REVIEW_PROBABILITY = 0.50
SQL_FILENAME = 'generated_reviews.sql'

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# ---------------- ACTIVATE TICKETS ----------------
cursor.execute("""
    SELECT t.ID
    FROM Ticket t
    JOIN Event e ON t.Event_ID = e.ID
    JOIN Spectator s ON t.ID = s.Ticket_ID
    WHERE e.Start_Time < NOW()
    AND s.Visitor_ID IS NOT NULL
    AND t.Activated = FALSE
""")
tickets_to_consider = [row[0] for row in cursor.fetchall()]
random.shuffle(tickets_to_consider)

activated_count = 0
for ticket_id in tickets_to_consider:
    if random.random() < ACTIVATION_PROBABILITY:
        cursor.execute("UPDATE Ticket SET Activated = TRUE WHERE ID = %s", (ticket_id,))
        activated_count += 1

conn.commit()
print(f"Activated {activated_count} tickets (~95% of eligible).")

# ---------------- SELECT FOR REVIEWS ----------------
cursor.execute("""
    SELECT t.ID
    FROM Ticket t
    JOIN Spectator s ON t.ID = s.Ticket_ID
    WHERE t.Activated = TRUE
    AND t.Date_Bought IS NOT NULL
""")
eligible_review_tickets = [row[0] for row in cursor.fetchall()]
random.shuffle(eligible_review_tickets)

review_candidates = [
    ticket_id for ticket_id in eligible_review_tickets
    if random.random() < REVIEW_PROBABILITY
]

# ---------------- GENERATE REVIEWS ----------------
reviews = []
for ticket_id in review_candidates:
    review = (
        random.randint(1, 5),  # Interpretation
        random.randint(1, 5),  # Sound
        random.randint(1, 5),  # Lighting
        random.randint(1, 5),  # Stage Presence
        random.randint(1, 5),  # Organization
        random.randint(1, 5),  # Overall
        ticket_id
    )
    reviews.append(review)

# ---------------- INSERT INTO DB ----------------
insert_sql = """
INSERT INTO Review (Interpretation, Sound, Lighting, Stage_Presence, Organization, Overall, Ticket_ID)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

try:
    if reviews:
        cursor.executemany(insert_sql, reviews)
        conn.commit()
        print(f"Inserted {cursor.rowcount} reviews (~50% of activated tickets).")
    else:
        print("No reviews inserted. No tickets met the 50% review chance.")
except mysql.connector.Error as err:
    print(f"Error inserting reviews: {err}")

# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(reviews, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Review table\n')
        for r in reviews:
            stmt = (
                "INSERT INTO Review (Interpretation, Sound, Lighting, Stage_Presence, Organization, Overall, Ticket_ID) "
                f"VALUES ({r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]}, {r[6]});\n"
            )
            f.write(stmt)

# ---------------- CLEAN UP ----------------
cursor.close()
conn.close()
print("Database connection closed.")

# ---------------- MAIN ----------------
def main():
    if reviews:
        write_sql_file(reviews, SQL_FILENAME)

if __name__ == '__main__':
    main()
