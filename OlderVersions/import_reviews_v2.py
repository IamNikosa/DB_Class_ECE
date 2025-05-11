import random
import mysql.connector

# ---------------- CONFIG ----------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Festival'
}

ACTIVATION_PROBABILITY = 0.95
REVIEW_PROBABILITY = 0.30

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Step 1: Activate ~95% of eligible tickets (for past events & sold)
cursor.execute("""
    SELECT t.ID
    FROM Ticket t
    JOIN Event e ON t.Event_ID = e.ID
    JOIN Spectator s ON t.ID = s.Ticket_ID
    WHERE e.Start_Time < NOW()
    AND s.Visitor_ID IS NOT NULL
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

# Step 2: Fetch activated tickets with owners (Spectator) for reviews
cursor.execute("""
    SELECT t.ID
    FROM Ticket t
    JOIN Spectator s ON t.ID = s.Ticket_ID
    WHERE t.Activated = TRUE
    AND t.Date_Bought IS NOT NULL
""")
eligible_review_tickets = [row[0] for row in cursor.fetchall()]
random.shuffle(eligible_review_tickets)

# Step 3: Choose ~30% of activated tickets for reviews
review_candidates = [
    ticket_id for ticket_id in eligible_review_tickets
    if random.random() < REVIEW_PROBABILITY
]

# Step 4: Generate reviews
reviews = []
for ticket_id in review_candidates:
    review = (
        random.randint(6, 10),  # Interpretation
        random.randint(6, 10),  # Sound
        random.randint(6, 10),  # Lighting
        random.randint(6, 10),  # Stage Presence
        random.randint(6, 10),  # Organization
        random.randint(6, 10),  # Overall
        ticket_id
    )
    reviews.append(review)

# Step 5: Insert reviews
insert_query = """
INSERT INTO Review (Interpretation, Sound, Lighting, Stage_Presence, Organization, Overall, Ticket_ID)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

try:
    if reviews:
        cursor.executemany(insert_query, reviews)
        conn.commit()
        print(f"Inserted {cursor.rowcount} reviews (~30% of activated tickets).")
    else:
        print("No reviews inserted. No tickets met the 30% review chance.")
except mysql.connector.Error as err:
    print(f"Error inserting reviews: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
