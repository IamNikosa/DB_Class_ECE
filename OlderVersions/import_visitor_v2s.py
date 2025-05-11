import mysql.connector
from faker import Faker
import random

# ---------------- CONFIG ----------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # change this
    'database': 'Fest'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Number of visitors to create
NUM_VISITORS = 2000

visitor_data = []

for visitor_id in range(1, NUM_VISITORS + 1):
    first_name = fake.first_name().replace("'", "''")
    last_name = fake.last_name().replace("'", "''")
    age = random.randint(16, 70)
    con_info = fake.email()

    visitor_data.append((visitor_id, first_name, last_name, age, con_info))

# Insert data
insert_query = """
INSERT INTO Visitor (ID, First_Name, Last_Name, Age, Con_Info)
VALUES (%s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_query, visitor_data)
    conn.commit()
    print(f"{cursor.rowcount} visitors inserted successfully.")
except mysql.connector.Error as err:
    print(f"Database error: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
