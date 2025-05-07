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

# Predefined genre names (you can expand this list)
genre_names = [
    'Rock', 'Jazz', 'Classical', 'Hip Hop', 'Electronic', 'Pop',
    'Folk', 'Blues', 'Reggae', 'Metal', 'Punk', 'Country',
    'Soul', 'Funk', 'Techno', 'Opera', 'R&B', 'Indie', 'House', 'Trance'
]

# Remove duplicates in case the table already has entries
cursor.execute("SELECT Name FROM Genre")
existing = {row[0] for row in cursor.fetchall()}
new_genres = [g for g in genre_names if g not in existing]

# Insert new genres with manual IDs (since no AUTO_INCREMENT)
start_id = 1
cursor.execute("SELECT MAX(ID) FROM Genre")
row = cursor.fetchone()
if row[0] is not None:
    start_id = row[0] + 1

genre_data = [(start_id + i, name) for i, name in enumerate(new_genres)]

insert_query = "INSERT INTO Genre (ID, Name) VALUES (%s, %s)"

try:
    cursor.executemany(insert_query, genre_data)
    conn.commit()
    print(f"Inserted {cursor.rowcount} genres.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()
    print("Connection closed.")
