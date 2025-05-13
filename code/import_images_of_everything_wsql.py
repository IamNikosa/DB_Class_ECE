#!/usr/bin/env python3
"""
import_images_of_everything_wsql.py

Inserts fake image records into the Image table and links them
to various entities (Festival, Performer, etc.) via join tables.
Writes all INSERT statements to a .sql file.
"""
import os
import random
from faker import Faker
import mysql.connector
from datetime import datetime

# ---------------- SETUP ----------------
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ---------------- CONFIG ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'festival'
}
SQL_FILENAME = 'generated_images.sql'
TOTAL_IMAGES = 100

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Initialize Faker
epoch_seed = int(datetime.now().timestamp())
fake = Faker()
Faker.seed(epoch_seed)
random.seed(epoch_seed)

# ---------------- HELPER ----------------
def fetch_ids(table, column='ID'):
    cursor.execute(f"SELECT {column} FROM {table}")
    return [row[0] for row in cursor.fetchall()]

# ---------------- ENTITY LINK TABLES ----------------
image_links = {
    'Festival': 'Festival_Image',
    'Performer': 'Performer_Image',
    'Stage': 'Stage_Image',
    'Staff': 'Staff_Image',
    'Event': 'Event_Image',
    'Location': 'Location_Image'
}

# ---------------- INSERT IMAGES ----------------
images = [(fake.image_url(), fake.sentence(nb_words=6)) for _ in range(TOTAL_IMAGES)]

insert_sql = "INSERT INTO Image (URL, Description) VALUES (%s, %s)"
cursor.executemany(insert_sql, images)
conn.commit()
print(f"Inserted {cursor.rowcount} images into the database.")

# Fetch inserted Image IDs in original insert order
cursor.execute("SELECT ID FROM Image ORDER BY ID DESC LIMIT %s", (TOTAL_IMAGES,))
image_ids = [row[0] for row in cursor.fetchall()][::-1]

# ---------------- WRITE TO SQL FILE ----------------
with open(SQL_FILENAME, 'w', encoding='utf-8') as f:
    f.write('-- INSERTs into Image table\n')
    for i, (url, desc) in enumerate(images):
        desc_escaped = desc.replace("'", "''")
        f.write(f"INSERT INTO Image (URL, Description) VALUES ('{url}', '{desc_escaped}');\n")

    # ---------------- LINK IMAGES TO ENTITIES ----------------
    for table, link_table in image_links.items():
        entity_ids = fetch_ids(table)
        if not entity_ids:
            print(f"Skipping {table} (no records).")
            continue

        links = []
        for entity_id in entity_ids:
            num_images = random.randint(1, 3)
            assigned = random.sample(image_ids, min(num_images, len(image_ids)))
            for img_id in assigned:
                links.append((entity_id, img_id))

        entity_col = f"{table}_ID"
        link_insert_sql = f"INSERT IGNORE INTO {link_table} ({entity_col}, Image_ID) VALUES (%s, %s)"

        try:
            cursor.executemany(link_insert_sql, links)
            conn.commit()
            print(f"Linked {cursor.rowcount} images to {table}.")
        except mysql.connector.Error as err:
            print(f"Error linking images to {table}: {err}")

        # Write to .sql file
        f.write(f"\n-- INSERTs into {link_table}\n")
        for entity_id, image_id in links:
            f.write(
                f"INSERT IGNORE INTO {link_table} ({entity_col}, Image_ID) "
                f"VALUES ({entity_id}, {image_id});\n"
            )

# ---------------- CLEAN UP ----------------
cursor.close()
conn.close()
print("All images inserted and linked successfully.")
