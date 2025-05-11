import random
import mysql.connector
from faker import Faker
import datetime

# ---------------- CONFIG ----------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'festival'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
conn.autocommit = True
cursor = conn.cursor()

# ---------------- CLEAN UP EXISTING DATA ----------------
# Disable foreign‑key checks temporarily to avoid constraint errors
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

# Delete dependent rows first, then parent rows
cursor.execute("DELETE FROM Event")

# Re‑enable foreign‑key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Initialize Faker
fake = Faker()
import time
Faker.seed(int(time.time()))
random.seed(int(time.time()))

# ---------------- HELPER FUNCTIONS ----------------

fake = Faker()
Faker.seed(0)
random.seed(0)

cursor.execute("SELECT ID FROM Location")
locations = cursor.fetchall()

def generate_festival_data(i):
    # Generate a fake festival
    name = fake.word().capitalize() + " Festival"  # e.g., "Music Festival"
    
    # Randomize the year for the festival
    year = 2018 + i  # Pick a random year from a set

    # Create start and end dates within the selected year
    start_date = fake.date_between(start_date=datetime.date(year, 6, 1), end_date=datetime.date(year, 9, 1))
    end_date = fake.date_between(start_date=start_date, end_date=datetime.date(year, 9, 30))
    
    location_id = locations[i][0]  # Extract the ID value from the tuple
    if location_id is None:
        raise ValueError("No location found in the Location table. Please insert some locations first.")
    
    return (name, start_date, end_date, location_id, year)

# ---------------- GENERATE FESTIVALS ----------------

NUM_FESTIVALS = 10
festival_values = []

for i in range(NUM_FESTIVALS):
    try:
        festival = generate_festival_data(i)
        festival_values.append(festival)
    except Exception as e:
        print(f"Error generating festival: {e}")

# Insert Festival Data into DB
if festival_values:
    festival_sql = "INSERT INTO `Festival` (`Name`, `Start_Date`, `End_Date`, `Location_ID`, `Year`) VALUES\n"
    festival_sql += ",\n".join([f"('{festival[0]}', '{festival[1]}', '{festival[2]}', {festival[3]}, {festival[4]})" for festival in festival_values])
    festival_sql += ";"
    
    try:
        cursor.execute(festival_sql)
        print(f"Successfully inserted {NUM_FESTIVALS} festivals.")
    except mysql.connector.Error as err:
        print(f"Error inserting festival data into database: {err}")

# Ensure cursor and connection are closed
if cursor:
    cursor.close()
    print("Database cursor closed.")
if conn and conn.is_connected():
    conn.close()
    print("Database connection closed.")
