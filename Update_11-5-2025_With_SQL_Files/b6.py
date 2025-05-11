import mysql.connector
import time
start_time=time.time()

visitor_id = 1  

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='xaua6709ni!',
    database='Festival'
)
cursor = conn.cursor()

query = """
SELECT 
    e.ID AS Event_ID,
    f.Name AS Festival_Name,
    e.Start_Time,
    AVG(r.Overall) AS Avg_Overall_Score
FROM Spectator sp
JOIN Ticket t ON sp.Ticket_ID = t.ID
JOIN Event e ON t.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
JOIN Review r ON r.Ticket_ID = t.ID
WHERE sp.Visitor_ID = %s
GROUP BY e.ID
ORDER BY e.Start_Time;
"""

cursor.execute(query, (visitor_id,))
rows = cursor.fetchall()

end_time = time.time()
execution_time = end_time - start_time

if rows:
    print(f"Visitor {visitor_id} — attended events and their average reviews:")
    for row in rows:
        print(f"Event ID: {row[0]} | Festival: {row[1]} | Start: {row[2]} | Avg Review: {round(row[3], 2)}")
else:
    print(f"No reviews found for visitor {visitor_id}")

print(f"\nQuery executed in {execution_time:.4f} seconds.")

cursor.close()
conn.close()
