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

query = """
SELECT 
    DATE(e.Start_Time) AS Festival_Date,
    CEIL(COUNT(sp.Visitor_ID) * 0.05) AS Required_Security,
    CEIL(COUNT(sp.Visitor_ID) * 0.02) AS Required_Support
FROM Event e
JOIN Ticket t ON e.ID = t.Event_ID
JOIN Spectator sp ON sp.Ticket_ID = t.ID
GROUP BY DATE(e.Start_Time)
ORDER BY Festival_Date;
"""

cursor.execute(query)
rows = cursor.fetchall()

end_time = time.time()
execution_time = end_time - start_time

if rows:
    print("Ημερήσιες ανάγκες προσωπικού (ανά κατηγορία):\n")
    print("Ημερομηνία | Security | Support")
    print("-" * 35)
    for row in rows:
        print(f"{row[0]} | {row[1]} άτομα | {row[2]} άτομα")
else:
    print("Δεν υπάρχουν δεδομένα παρακολούθησης για να υπολογιστεί προσωπικό.")

print(f"\nQuery executed in {execution_time:.4f} seconds.")

cursor.close()
conn.close()
