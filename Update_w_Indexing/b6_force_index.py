import mysql.connector
import time
start = time.time()

visitor_id = 267  # <-- άλλαξέ το σε όποιον επισκέπτη θες

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

query = """
SELECT 
    e.ID AS Event_ID,
    f.Name AS Festival_Name,
    e.Start_Time,
    AVG(r.Interpretation + r.Sound + r.Lighting + r.Stage_Presence + r.Organization + r.Overall) AS Avg_Overall_Score
FROM Spectator sp FORCE INDEX (idx_visitor_ticket)
JOIN Ticket t FORCE INDEX (PRIMARY) ON t.ID = sp.Ticket_ID 
JOIN Event e FORCE INDEX (PRIMARY) ON e.ID = t.Event_ID 
JOIN Festival f FORCE INDEX (PRIMARY) ON f.ID = e.Festival_ID 
JOIN Review r FORCE INDEX (idx_review_ticket) ON t.ID = r.Ticket_ID 
WHERE sp.Visitor_ID = %s
GROUP BY e.ID
ORDER BY e.Start_Time;
"""

cursor.execute(query, (visitor_id,))
rows = cursor.fetchall()

if rows:
    print(f"Visitor {visitor_id} — Attended events and their average reviews (out of 30):")
    for row in rows:
        print(f"Event ID: {row[0]} | Festival: {row[1]} | Start: {row[2]} | Avg Review (out of 30): {round(row[3], 2)}")
else:
    print(f"No reviews found for visitor {visitor_id}")

cursor.close()
conn.close()

print(f"\nElapsed time: {time.time() - start:.4f} seconds")

