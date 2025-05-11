import mysql.connector
import time
start_time=time.time()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='xaua6709ni!',
    database='Festival'
)
cursor = conn.cursor()

artist_name = 'Sandra Simon'

query = f"""
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    AVG(r.Interpretation) AS Avg_Interpretation,
    AVG(r.Overall) AS Avg_Overall
FROM Performer pe
JOIN Performance p ON pe.ID = p.Performer_ID
JOIN Event e ON p.Event_ID = e.ID
JOIN Ticket t ON e.ID = t.Event_ID
JOIN Review r ON r.Ticket_ID = t.ID
WHERE pe.Stage_Name = %s
GROUP BY pe.ID;
"""

cursor.execute(query, (artist_name,))
row = cursor.fetchone()

end_time = time.time()
execution_time = end_time - start_time

if row:
    print("Performer ID:", row[0])
    print("Stage Name:", row[1])
    print("Average Interpretation:", round(row[2], 2))
    print("Average Overall:", round(row[3], 2))
else:
    print(f"No reviews found for artist: {artist_name}")


print(f"\nQuery executed in {execution_time:.4f} seconds.")

cursor.close()
conn.close()
