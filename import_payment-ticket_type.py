import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Fest'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Data to insert
payment_methods = ['Credit Card', 'PayPal', 'Cash', 'Bank Transfer']
ticket_types = ['VIP', 'Standard', 'Student', 'Backstage']

# Insert into Payment
for method in payment_methods:
    try:
        cursor.execute("INSERT INTO Payment (Name) VALUES (%s)", (method,))
    except mysql.connector.Error as err:
        print(f"Error inserting payment method '{method}': {err}")

# Insert into Type
for ticket_type in ticket_types:
    try:
        cursor.execute("INSERT INTO Type (Name) VALUES (%s)", (ticket_type,))
    except mysql.connector.Error as err:
        print(f"Error inserting ticket type '{ticket_type}': {err}")

# Commit and close
conn.commit()
cursor.close()
conn.close()
print("Inserted payment methods and ticket types successfully.")
