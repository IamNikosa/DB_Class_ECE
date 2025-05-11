import mysql.connector
from faker import Faker
import random

# ---------------- CONFIG ----------------
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
def calculate_ean13_check_digit(ean12):
    """
    Calculate the EAN-13 check digit for a 12-digit number.
    :param ean12: A string of 12 digits.
    :return: A single check digit as a string.
    """
    if len(ean12) != 12 or not ean12.isdigit():
        raise ValueError("Input must be a 12-digit numeric string.")

    total = 0
    for i, digit in enumerate(ean12):
        num = int(digit)
        if (i + 1) % 2 == 0:  # Even position (2nd, 4th, ..., 12th)
            total += num * 3
        else:  # Odd position (1st, 3rd, ..., 11th)
            total += num

    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)

def generate_ean13(ticket_id):
    """
    Generate a valid EAN-13 code using the ticket ID.
    :param ticket_id: Integer representing the ticket ID.
    :return: A 13-digit EAN-13 code as a string.
    """
    prefix = '200'  # Custom prefix for your organization
    company_code = '0001'  # Example company code
    product_code = str(ticket_id).zfill(5)  # Zero-padded to ensure 5 digits

    ean12 = prefix + company_code + product_code
    check_digit = calculate_ean13_check_digit(ean12)
    return ean12 + check_digit

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
                # Insert a placeholder ticket to get the auto-incremented ID
                cursor.execute(
                    """
                    INSERT INTO Ticket
                    (EAN_CODE, Stage_Info, Price, Activated, Date_Bought, Type_ID, Payment_ID, Event_ID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    ('', stage_info, price, activated, date_bought, chosen_type, payment_id, event_id)
                )
                ticket_id = cursor.lastrowid
                ean_code = generate_ean13(ticket_id)

                # Update the ticket with the generated EAN code
                cursor.execute(
                    "UPDATE Ticket SET EAN_CODE = %s WHERE ID = %s",
                    (ean_code, ticket_id)
                )
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
