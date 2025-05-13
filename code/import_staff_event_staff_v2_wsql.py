#!/usr/bin/env python3
"""
import_staff_event_staff_v2_wsql.py

Generates staff members and assigns them to events based on stage capacity.
Populates Staff, role-specific tables, and event_staff.
Also writes all generated INSERTs to a .sql file.
"""
import os
import math
import random
from faker import Faker
import mysql.connector

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
SQL_FILENAME = 'generated_event_staff.sql'

STAFF_TYPES = ['Trainee', 'Beginner', 'Intermediate', 'Experienced', 'Very Experienced']
SECURITY_RATIO = 0.05
SUPPORT_RATIO = 0.02
TECHNICAL_RATIO = 0.03

# ---------------- CONNECT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
conn.autocommit = True
cursor = conn.cursor()

# ---------------- INITIALIZE ----------------
fake = Faker()
Faker.seed(0)
random.seed(0)

# ---------------- CLEAN EXISTING DATA ----------------
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DELETE FROM event_staff")
cursor.execute("DELETE FROM Security_Staff")
cursor.execute("DELETE FROM Support_Staff")
cursor.execute("DELETE FROM Technical_Staff")
cursor.execute("DELETE FROM Staff")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# ---------------- FETCH EVENTS ----------------
cursor.execute("""
    SELECT E.ID, E.Stage_ID, S.Capacity
    FROM Event E
    JOIN Stage S ON E.Stage_ID = S.ID
""")
events = cursor.fetchall()
if not events:
    print("No events found. Exiting.")
    cursor.close()
    conn.close()
    exit()

# ---------------- GENERATE STAFF ----------------
staff_id = 1
staff_rows = []
role_inserts = []
security_staff, support_staff, technical_staff = [], [], []

for event_id, stage_id, capacity in events:
    num_security = math.ceil(capacity * SECURITY_RATIO)
    num_support = math.ceil(capacity * SUPPORT_RATIO)
    num_technical = math.ceil(capacity * TECHNICAL_RATIO)

    for _ in range(num_security):
        name = fake.name().replace("'", "''")
        age = random.randint(20, 60)
        type_ = random.choice(STAFF_TYPES)
        staff_rows.append((staff_id, name, age, type_))
        role_inserts.append(f"INSERT INTO Security_Staff (Staff_ID) VALUES ({staff_id});")
        security_staff.append(staff_id)
        staff_id += 1

    for _ in range(num_support):
        name = fake.name().replace("'", "''")
        age = random.randint(20, 60)
        type_ = random.choice(STAFF_TYPES)
        staff_rows.append((staff_id, name, age, type_))
        role_inserts.append(f"INSERT INTO Support_Staff (Staff_ID) VALUES ({staff_id});")
        support_staff.append(staff_id)
        staff_id += 1

    for _ in range(num_technical):
        name = fake.name().replace("'", "''")
        age = random.randint(20, 60)
        type_ = random.choice(STAFF_TYPES)
        staff_rows.append((staff_id, name, age, type_))
        role_inserts.append(f"INSERT INTO Technical_Staff (Staff_ID) VALUES ({staff_id});")
        technical_staff.append(staff_id)
        staff_id += 1

print(f"Generated {len(staff_rows)} staff members.")

# ---------------- WRITE & INSERT STAFF ----------------
with open(SQL_FILENAME, 'w', encoding='utf-8') as f:
    f.write('-- Insert into Staff table\n')
    f.write("INSERT INTO Staff (ID, Name, Age, Type) VALUES\n")
    f.write(",\n".join(f"({sid}, '{name}', {age}, '{typ}')" for sid, name, age, typ in staff_rows))
    f.write(";\n\n")

    insert_staff_sql = (
        "INSERT INTO Staff (ID, Name, Age, Type) VALUES (%s, %s, %s, %s)"
    )
    try:
        cursor.executemany(insert_staff_sql, staff_rows)
    except mysql.connector.Error as err:
        print(f"Error inserting into Staff: {err}")

    # ---------------- WRITE & INSERT ROLE TABLES ----------------
    f.write('-- Insert into role-specific tables\n')
    for role_sql in role_inserts:
        f.write(role_sql + '\n')
        try:
            cursor.execute(role_sql)
        except mysql.connector.Error as err:
            print(f"Error inserting role: {err}")
    f.write("\n")

    # ---------------- ASSIGN STAFF TO EVENTS ----------------
    f.write('-- Assign staff to events\n')
    event_staff_rows = []
    inserted_pairs = set()

    def get_stage_capacity(stage_id):
        cursor.execute("SELECT Capacity FROM Stage WHERE ID = %s", (stage_id,))
        result = cursor.fetchone()
        return result[0] if result else 0

    for event_id, stage_id in [(e[0], e[1]) for e in events]:
        capacity = get_stage_capacity(stage_id)
        assigned = set()

        for group, ratio in [
            (security_staff, SECURITY_RATIO),
            (support_staff, SUPPORT_RATIO),
            (technical_staff, TECHNICAL_RATIO)
        ]:
            needed = math.ceil(capacity * ratio)
            available = [s for s in group if s not in assigned]
            for sid in random.sample(available, min(needed, len(available))):
                if (sid, event_id) not in inserted_pairs:
                    event_staff_rows.append((sid, event_id))
                    inserted_pairs.add((sid, event_id))
                    assigned.add(sid)

    if event_staff_rows:
        f.write("INSERT INTO event_staff (Staff_ID, Event_ID) VALUES\n")
        f.write(",\n".join(f"({sid}, {eid})" for sid, eid in event_staff_rows))
        f.write(";\n")

        try:
            cursor.executemany(
                "INSERT INTO event_staff (Staff_ID, Event_ID) VALUES (%s, %s)",
                event_staff_rows
            )
        except mysql.connector.Error as err:
            print(f"Error inserting into event_staff: {err}")

# ---------------- CLEAN UP ----------------
cursor.close()
conn.close()
print("All staff data inserted and SQL file generated.")
