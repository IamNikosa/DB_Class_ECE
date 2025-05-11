import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Constants
NUM_PERFORMERS = 80

try:
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'festival'
    }

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Faker and random seed setup
    fake = Faker()
    import time
    Faker.seed(int(time.time()))
    random.seed(int(time.time()))

    # Data containers
    performers = []
    bands = []
    solo_artists = []

    # Generate performers
    for i in range(NUM_PERFORMERS):
        is_band = random.choice([True, False])
        real_name = fake.name() if not is_band else None
        stage_name = fake.word().capitalize() + " Band" if is_band else fake.first_name() + " " + fake.last_name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=60) if not is_band else None
        formation_date = fake.date_between(start_date='-30y', end_date='-1y') if is_band else None
        instagram = fake.user_name()
        website = fake.url()

        performer_id = i+1
        performers.append((
            performer_id, real_name, stage_name, birthday, instagram, website, is_band, formation_date
        ))

        if is_band:
            bands.append(i + 1)
        else:
            solo_artists.append(i + 1)

    # Insert performers (auto-incremented ID will be handled by MySQL)
    insert_query = """
    INSERT INTO Performer (ID, Real_Name, Stage_Name, Birthday, Instagram, Website, Is_Band, Formation_Date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, performers)
    conn.commit()
    print(f"{cursor.rowcount} performers inserted.")

    # Create memberships (solo artists in bands)
    memberships = []
    for artist_id in solo_artists:
        if bands and random.random() < 0.6:  # 60% chance
            band_id = random.choice(bands)
            # Ensure the membership doesn't already exist
            if (band_id, artist_id) not in [(m[0], m[1]) for m in memberships]:
                join_date = fake.date_between(start_date='-10y', end_date='today')
                memberships.append((band_id, artist_id, join_date))

    # Now, ensure each band gets at least one more solo artist (if there are enough artists)
    for band_id in bands:
        if len([m for m in memberships if m[0] == band_id]) == 1:  # If the band only has 1 member
            if solo_artists:  # Assign a second member if possible
                artist_id = random.choice(solo_artists)
                solo_artists.remove(artist_id)
                join_date = fake.date_between(start_date='-10y', end_date='today')
                memberships.append((band_id, artist_id, join_date))

    if memberships:
        membership_query = """
        INSERT INTO Membership (Band_ID, Artist_ID, Join_Date)
        VALUES (%s, %s, %s)
        """
        cursor.executemany(membership_query, memberships)
        conn.commit()
        print(f"{cursor.rowcount} membership rows inserted.")

except mysql.connector.Error as err:
    print(f"❌ Database error: {err}")
    if conn:
        conn.rollback()
except Exception as e:
    print(f"❌ Error: {e}")
    if conn:
        conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
