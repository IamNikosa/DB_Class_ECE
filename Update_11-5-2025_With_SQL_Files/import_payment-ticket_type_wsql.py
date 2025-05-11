#!/usr/bin/env python3
import os
import mysql.connector

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xaua6709ni!',
    'database': 'Festival'
}

# SQL output file name
SQL_FILENAME = 'generated_payment_and_types.sql'

# Lists of data to insert
db_payments = ['Credit Card', 'PayPal', 'Cash', 'Bank Transfer']
db_ticket_types = ['VIP', 'Standard', 'Student', 'Backstage']

# ---------------- SETUP ----------------
# Ensure script runs in its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Function to write SQL file
def write_sql_file(payments, ticket_types, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('-- Generated INSERTs for Payment and Type tables\n')
        for method in payments:
            method_esc = method.replace("'", "''")
            f.write(f"INSERT INTO Payment (Name) VALUES ('{method_esc}');\n")
        f.write('\n')
        for ttype in ticket_types:
            t_esc = ttype.replace("'", "''")
            f.write(f"INSERT INTO Type (Name) VALUES ('{t_esc}');\n")

# ---------------- MAIN ----------------
def main():
    # 1) Connect to DB
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 2) Insert Payment methods
    for method in db_payments:
        try:
            cursor.execute("INSERT INTO Payment (Name) VALUES (%s)", (method,))
        except mysql.connector.Error as err:
            print(f"Error inserting payment method '{method}': {err}")

    # 3) Insert Ticket types
    for ttype in db_ticket_types:
        try:
            cursor.execute("INSERT INTO Type (Name) VALUES (%s)", (ttype,))
        except mysql.connector.Error as err:
            print(f"Error inserting ticket type '{ttype}': {err}")

    # 4) Commit and close DB
    conn.commit()
    cursor.close()
    conn.close()
    print("Inserted payment methods and ticket types successfully.")

    # 5) Write .sql file
    write_sql_file(db_payments, db_ticket_types, SQL_FILENAME)

if __name__ == '__main__':
    main()
