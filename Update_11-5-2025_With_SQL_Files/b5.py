import mysql.connector
import time
start_time=time.time();

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='xaua6709ni!',
    database='Festival'
)
cursor = conn.cursor()

query = """
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    TIMESTAMPDIFF(YEAR, pe.Birthday, CURDATE()) AS Age,
    COUNT(DISTINCT f.ID) AS Festival_Count
FROM Performer pe
JOIN Performance p ON pe.ID = p.Performer_ID
JOIN Event e ON p.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
WHERE pe.Is_Band = FALSE
  AND TIMESTAMPDIFF(YEAR, pe.Birthday, CURDATE()) < 30
GROUP BY pe.ID
ORDER BY Festival_Count DESC;
"""

cursor.execute(query)
rows = cursor.fetchall()

end_time = time.time()
execution_time = end_time - start_time

print("Young performers (<30) with most festival appearances:")
for row in rows:
    print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Festivals: {row[3]}")

print(f"\nQuery executed in {execution_time:.4f} seconds.")

cursor.close()
conn.close()
