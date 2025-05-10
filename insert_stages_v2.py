import mysql.connector
from faker import Faker
import random

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'festival'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# ---------------- CLEAN UP EXISTING DATA ----------------
# Disable foreign‑key checks temporarily to avoid constraint errors
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

# Delete dependent rows first, then parent rows
cursor.execute("DELETE FROM Stage")

# Re‑enable foreign‑key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Initialize Faker
fake = Faker()
Faker.seed(1)
random.seed(1)

# Number of stages to generate
NUM_STAGES = 50

# Generate and insert stages
stage_data = []
for stage_id in range(1, NUM_STAGES + 1):
    name = fake.company() + " Stage"
    description = fake.sentence(nb_words=6)
    capacity = random.randint(100, 200)
    tech_info = fake.catch_phrase()

    stage_data.append((stage_id, name, description, capacity, tech_info))

# Insert into Stage table
insert_query = """
INSERT INTO Stage (ID, Name, Description, Capacity, Tech_Info)
VALUES (%s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_query, stage_data)
    conn.commit()
    print(f"{cursor.rowcount} fake stages inserted successfully.")
except mysql.connector.Error as err:
    print(f"Database error: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
