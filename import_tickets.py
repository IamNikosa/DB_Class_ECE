import mysql.connector
from faker import Faker
import random
from datetime import datetime

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

fake = Faker()
Faker.seed(123)
random.seed(123)

# ---------------- FETCH DEPENDENCIES ----------------

def fetch_events():
    cursor.execute("SELECT ID, Stage_ID FROM Event")
    return cursor.fetchall()

def fetch_types():
    cursor.execute("SELECT Name FROM Type")
    return [row[0] for row in cursor.fetchall()]

def fetch_payments():
    cursor.execute("SELECT Name FROM Payment")
    return [row[0] for row in cursor.fetchall()]

events = fetch_events()
types = fetch_types()
payments = fetch_payments()

if not events or not types or not payments:
    print("Ensure that Event, Type, and Payment tables are populated.")
    conn.close()
    exit()

# ---------------- GENERATE TICKETS ----------------

NUM_TICKETS = 300
ticket_values = []

for i in range(1, NUM_TICKETS + 1):
    event = random.choice(events)
    event_id = event[0]
    stage_id = event[1]
    
    ean_url = f"https://tickets.example.com/ean/{i}"
    stage_info = f"Entrance: Gate {random.randint(1, 5)}, Row {random.randint(1, 30)}"
    price = round(random.uniform(30, 150), 2)
    activated = random.choice([True, False])
    date_bought = fake.date_between(start_date='-1y', end_date='today')
    type_id = random.choice(types)
    payment_id = random.choice(payments)

    ticket_values.append((
        i, ean_url, stage_info, price, activated, date_bought, type_id, payment_id, event_id
    ))

# ---------------- INSERT TICKETS ----------------
insert_query = """
INSERT INTO Ticket
(ID, EAN_URL, Stage_Info, Price, Activated, Date_Bought, Type_ID, Payment_ID, Event_ID)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_query, ticket_values)
    conn.commit()
    print(f"{cursor.rowcount} fake tickets inserted successfully.")
except mysql.connector.Error as err:
    print(f"Database error: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")

