#!/usr/bin/env python3
"""
import_tickets.py

Generates fake ticket entries, inserts them into the Ticket table,
and writes corresponding INSERT statements to a .sql file
in the same directory as this script.
"""
import os
import random
import string
import mysql.connector
from faker import Faker
from datetime import datetime

# ---------------- SETUP ----------------
# Ensure script runs from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xaua6709ni!',
    'database': 'Festival'
}
SQL_FILENAME = 'generated_tickets.sql'

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Initialize Faker and random seed
epoch_seed = int(datetime.now().timestamp())
fake = Faker()
Faker.seed(epoch_seed)
random.seed(epoch_seed)

# ---------------- EAN-13 GENERATION ----------------
def calculate_ean13_check_digit(base12: str) -> str:
    total = 0
    for idx, digit_char in enumerate(reversed(base12), start=1):
        digit = int(digit_char)
        total += digit * (3 if idx % 2 == 0 else 1)
    return str((10 - (total % 10)) % 10)

def generate_ean13() -> str:
    base12 = ''.join(random.choices(string.digits, k=12))
    return base12 + calculate_ean13_check_digit(base12)

# ---------------- FETCH EVENT CAPACITIES ----------------
cursor.execute("""
    SELECT e.ID, s.Capacity
    FROM Event e
    JOIN Stage s ON e.Stage_ID = s.ID
""")
events = cursor.fetchall()

if not events:
    raise RuntimeError("No events found. Please ensure Event and Stage tables are populated.")

# ---------------- DEFAULT PRICING ----------------
default_prices = {
    'Student': 20.00,
    'Standard': 50.00,
    'Backstage': 80.00,
    'VIP': 120.00,
}
ticket_types = list(default_prices.keys())

# ---------------- GENERATE TICKETS ----------------
insert_sql = """
INSERT INTO Ticket (EAN_CODE, Stage_Info, Price, Activated, Date_Bought, Type_ID, Payment_ID, Event_ID)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

ticket_rows = []
ticket_rows_for_sql = []

for event_id, capacity in events:
    for _ in range(capacity):
        ean_code = generate_ean13()
        stage_info = f"Entrance: Gate {random.randint(1, 5)}, Row {random.randint(1, 30)}"
        price = None
        activated = False
        date_bought = None
        payment_id = None

        type_options = ticket_types.copy()
        while type_options:
            chosen_type = random.choice(type_options)
            price = default_prices[chosen_type]
            try:
                cursor.execute(insert_sql, (
                    ean_code, stage_info, price,
                    activated, date_bought, chosen_type,
                    payment_id, event_id
                ))
                conn.commit()
                ticket_rows.append((
                    ean_code, stage_info, price, activated,
                    date_bought, chosen_type, payment_id, event_id
                ))
                break
            except mysql.connector.Error as err:
                if 'VIP ticket limit' in str(err):
                    type_options = [t for t in type_options if t.upper() != 'VIP']
                else:
                    print(f"Error inserting ticket: {err}")
                    break


# ---------------- WRITE .SQL FILE ----------------
def write_sql_file(rows, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Ticket table\n')
        for row in rows:
            ean, info, price, activated, date_bought, type_id, pay_id, event_id = row
            activated_int = 1 if activated else 0
            stmt = (
                f"INSERT INTO Ticket (EAN_CODE, Stage_Info, Price, Activated, Date_Bought, Type_ID, Payment_ID, Event_ID) "
                f"VALUES ('{ean}', '{info}', {price}, {activated_int}, NULL, '{type_id}', NULL, {event_id});\n"
            )
            f.write(stmt)

# Clean up DB connections
cursor.close()
conn.close()
print("Database connection closed.")

# Finally write to .sql file
def main():
    write_sql_file(ticket_rows, SQL_FILENAME)

if __name__ == '__main__':
    main()
