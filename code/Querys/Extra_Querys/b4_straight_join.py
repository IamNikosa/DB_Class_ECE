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

artist_name = 'Heart Band' 

query = f"""
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    AVG(r.Interpretation) AS Avg_Interpretation,
    AVG(r.Overall) AS Avg_Overall
FROM Performer pe
STRAIGHT_JOIN Performance p ON pe.ID = p.Performer_ID
STRAIGHT_JOIN Event e ON p.Event_ID = e.ID
STRAIGHT_JOIN Ticket t ON e.ID = t.Event_ID
STRAIGHT_JOIN Review r ON r.Ticket_ID = t.ID
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

