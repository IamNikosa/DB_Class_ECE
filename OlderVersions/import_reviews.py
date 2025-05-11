import random
import mysql.connector

# ---------------- CONFIG ----------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Fest'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Fetch eligible Ticket_IDs (activated and owned)
cursor.execute("""
    SELECT t.ID
    FROM Ticket t
    JOIN Spectator s ON t.ID = s.Ticket_ID
    WHERE t.Activated = TRUE
""")
eligible_ticket_ids = [row[0] for row in cursor.fetchall()]
random.shuffle(eligible_ticket_ids)

# Limit how many reviews to insert
NUM_REVIEWS = min(30, len(eligible_ticket_ids))  # Or any number up to the number of eligible tickets

# Prepare review entries
reviews = []
for i in range(NUM_REVIEWS):
    ticket_id = eligible_ticket_ids[i]
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

# SQL insert
insert_query = """
INSERT INTO Review (Interpretation, Sound, Lighting, Stage_Presence, Organization, Overall, Ticket_ID)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Insert reviews
try:
    cursor.executemany(insert_query, reviews)
    conn.commit()
    print(f"Inserted {cursor.rowcount} reviews into the Review table.")
except mysql.connector.Error as err:
    print(f"Error inserting reviews: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")

