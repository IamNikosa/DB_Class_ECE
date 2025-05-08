import mysql.connector
from faker import Faker
import random
import string
from datetime import datetime

# ---------------- CONFIG ----------------
# Adjust credentials as needed
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Festival'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Initialize Faker and random seeds for reproducibility
fake = Faker()
Faker.seed(123)
random.seed(123)

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

# ---------------- FETCH DEPENDENCIES ----------------
def fetch_events_with_capacity():
    cursor.execute(
        """
        SELECT e.ID, s.Capacity
        FROM Event e
        JOIN Stage s ON e.Stage_ID = s.ID
        """
    )
    return cursor.fetchall()

# ---------------- DEFAULT PRICING ----------------
# Student cheapest, then Regular, then Backstage, then VIP
default_prices = {
    'Student': 20.00,
    'Standard': 50.00,
    'Backstage': 80.00,
    'VIP': 120.00,
}

types = list(default_prices.keys())

events = fetch_events_with_capacity()

if not events:
    print("Ensure that Event table is populated.")
    conn.close()
    exit()

# Prepare insert statement
insert_query = (
    """
    INSERT INTO Ticket
    (EAN_CODE, Stage_Info, Price, Activated, Date_Bought, Type_ID, Payment_ID, Event_ID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
)

for event_id, capacity in events:
    for _ in range(capacity):
        # Generate ticket data
        ean_code = generate_ean13()
        stage_info = f"Entrance: Gate {random.randint(1,5)}, Row {random.randint(1,30)}"
        activated = False
        date_bought = None
        payment_id = None

        # Randomly pick a ticket type; fallback if VIP limit reached
        type_options = types.copy()
        while type_options:
            chosen_type = random.choice(type_options)
            price = default_prices[chosen_type]
            try:
                cursor.execute(insert_query, (
                    ean_code, stage_info, price,
                    activated, date_bought, chosen_type, payment_id, event_id
                ))
                conn.commit()
                break
            except mysql.connector.Error as err:
                err_msg = str(err)
                # Handle VIP limit error by retrying without VIP
                if 'VIP ticket limit' in err_msg:
                    type_options = [t for t in type_options if t.upper() != 'VIP']
                    continue
                else:
                    print(f"Error inserting ticket: {err_msg}")
                    break

cursor.close()
conn.close()
print("Ticket generation complete.")
