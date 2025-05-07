import mysql.connector
from faker import Faker
import random
from datetime import date, timedelta

# DB config
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Fest"
)
cursor = conn.cursor()

fake = Faker()
Faker.seed(1)
random.seed(1)

NUM_PERFORMERS = 50
performers = []

for i in range(NUM_PERFORMERS):
    is_band = random.choice([True, False])
    real_name = fake.name() if not is_band else None
    stage_name = fake.word().capitalize() + " Band" if is_band else fake.first_name() + " " + fake.last_name()
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=60) if not is_band else None
    formation_date = fake.date_between(start_date='-30y', end_date='-1y') if is_band else None
    instagram = fake.user_name()
    website = fake.url()

    performers.append((
        i + 1, real_name, stage_name, birthday, instagram, website, is_band, formation_date
    ))

insert_query = """
INSERT INTO Performer (ID, Real_Name, Stage_Name, Birthday, Instagram, Website, Is_Band, Formation_Date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, performers)
conn.commit()
print(f"{cursor.rowcount} performers inserted.")
cursor.close()
conn.close()
