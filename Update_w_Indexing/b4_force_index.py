import mysql.connector
import time
start = time.time()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

artist_name = 'Carolyn Hall'  # <-- Βάλε εδώ το όνομα που σε ενδιαφέρει

query = f"""
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    AVG(r.Interpretation) AS Avg_Interpretation,
    AVG(r.Overall) AS Avg_Overall
FROM Performer pe
JOIN Performance p FORCE INDEX (idx_performance_performer) ON pe.ID = p.Performer_ID
JOIN Event e FORCE INDEX (PRIMARY) ON e.ID = p.Event_ID
JOIN Ticket t FORCE INDEX (idx_ticket_event) ON e.ID = t.Event_ID
JOIN Review r FORCE INDEX (idx_review_ticket) ON t.ID = r.Ticket_ID 
WHERE pe.Stage_Name = %s
GROUP BY pe.ID;
"""

cursor.execute(query, (artist_name,))
row = cursor.fetchone()

if row:
    print("Performer ID:", row[0])
    print("Stage Name:", row[1])
    print("Average Interpretation:", round(row[2], 2))
    print("Average Overall:", round(row[3], 2))
else:
    print(f"No reviews found for artist: {artist_name}")

cursor.close()
conn.close()

print(f"\nElapsed time: {time.time() - start:.4f} seconds")
