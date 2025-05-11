#!/usr/bin/env python3
import os
import random
import mysql.connector
from faker import Faker

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xaua6709ni!',
    'database': 'Festival'
}

# Number of locations to generate
NUM_LOCATIONS = 20  # Change as needed

# SQL output file name
SQL_FILENAME = 'generated_locations.sql'

# ---------------- SETUP ----------------
# Ensure script runs from its own directory so files are written here
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialize Faker
fake = Faker()
Faker.seed(42)

# Function to generate random latitude and longitude
def generate_lat_lon():
    lat = round(random.uniform(-90.0, 90.0), 6)
    lon = round(random.uniform(-180.0, 180.0), 6)
    return lat, lon

# Generate random locations
def generate_locations(n):
    locations = []
    for _ in range(n):
        name = fake.company().replace("'", "''")
        city = fake.city().replace("'", "''")
        country = fake.country().replace("'", "''")
        continent = fake.random.choice([
            'Asia', 'Europe', 'North America', 'South America', 'Africa', 'Australia/Oceania'
        ])
        address = fake.address().replace("\n", ", ").replace("'", "''")
        latitude, longitude = generate_lat_lon()
        locations.append((name, latitude, longitude, address, city, country, continent))
    return locations

# Write SQL file with INSERT statements
def write_sql_file(locations_with_ids, filename):
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('/* Generated INSERT statements for Location table */\n')
        for loc in locations_with_ids:
            id_, name, lat, lon, address, city, country, continent = loc
            stmt = (
                "INSERT INTO Location "
                "(ID, Name, Latitude, Longitude, Address, City, Country, Continent) VALUES "
                f"({id_}, '{name}', {lat}, {lon}, '{address}', '{city}', '{country}', '{continent}');\n"
            )
            f.write(stmt)

# Main execution
def main():
    # 1) Generate data
    raw_locations = generate_locations(NUM_LOCATIONS)

    # 2) Assign IDs starting at 1
    locations_with_ids = [(i + 1, *loc) for i, loc in enumerate(raw_locations)]

    # 3) Insert into DB
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    insert_query = (
        "INSERT INTO Location "
        "(ID, Name, Latitude, Longitude, Address, City, Country, Continent) VALUES "
        "(%s, %s, %s, %s, %s, %s, %s, %s)"
    )
    try:
        cursor.executemany(insert_query, locations_with_ids)
        conn.commit()
        print(f"Inserted {cursor.rowcount} fake locations into the database.")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error inserting locations: {err}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

    # 4) Write .sql file in script directory
    write_sql_file(locations_with_ids, SQL_FILENAME)

if __name__ == '__main__':
    main()
