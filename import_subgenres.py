from faker import Faker
import random
import mysql.connector

# ---------------- CONFIG ----------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Fest'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
fake = Faker()
Faker.seed(42)

# Get existing Genre IDs
cursor.execute("SELECT ID FROM Genre")
genre_ids = [row[0] for row in cursor.fetchall()]
if not genre_ids:
    raise Exception("No genres found — cannot assign subgenres.")

# Get existing Subgenre names
cursor.execute("SELECT Name FROM Subgenre")
existing_subgenre_names = {row[0] for row in cursor.fetchall()}

# Base subgenre names
base_subgenre_names = [
    'Synthpop', 'Death Metal', 'Smooth Jazz', 'Trap', 'Indie Rock',
    'Electro Swing', 'Boom Bap', 'Grime', 'Neo Soul', 'Dub',
    'Tech House', 'Ska Punk', 'Drum and Bass', 'Tango Nuevo',
    'Opera Buffa', 'Post-Rock', 'Shoegaze', 'Trip Hop', 'Bossa Nova',
    'Glitch Hop', 'Vaporwave', 'Chillwave', 'Black Metal', 'Space Jazz'
]

# Combine base and dynamically generated names
subgenre_names = []
used_names = existing_subgenre_names.copy()
while len(subgenre_names) < 20:
    if base_subgenre_names:
        name = base_subgenre_names.pop(0)
    else:
        name = fake.unique.word().title() + " " + random.choice(["Style", "Wave", "Core", "Beats"])
    if name not in used_names:
        subgenre_names.append(name)
        used_names.add(name)

# Get starting ID
cursor.execute("SELECT MAX(ID) FROM Subgenre")
row = cursor.fetchone()
start_id = row[0] + 1 if row[0] is not None else 1

# Build data with random Genre_IDs
subgenre_data = [
    (start_id + i, name, random.choice(genre_ids))
    for i, name in enumerate(subgenre_names)
]

# Insert query
insert_query = "INSERT INTO Subgenre (ID, Name, Genre_ID) VALUES (%s, %s, %s)"

try:
    cursor.executemany(insert_query, subgenre_data)
    conn.commit()
    print(f"Inserted {cursor.rowcount} subgenres.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()
    print("Connection closed.")


