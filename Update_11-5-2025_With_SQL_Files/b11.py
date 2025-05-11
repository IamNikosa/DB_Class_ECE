import mysql.connector
import time
start_time=time.time()

# Connect to database
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
    COUNT(DISTINCT f.ID) AS Festival_Count
FROM Performer pe
JOIN Performance p ON pe.ID = p.Performer_ID
JOIN Event e ON p.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
GROUP BY pe.ID
HAVING Festival_Count <= (
    SELECT MAX(Festivals) - 5
    FROM (
        SELECT COUNT(DISTINCT f.ID) AS Festivals
        FROM Performance p
        JOIN Event e ON p.Event_ID = e.ID
        JOIN Festival f ON e.Festival_ID = f.ID
        GROUP BY p.Performer_ID
    ) AS subquery
)
ORDER BY Festival_Count ASC;
"""

cursor.execute(query)
rows = cursor.fetchall()

end_time = time.time()
execution_time = end_time - start_time

if rows:
    print("Καλλιτέχνες με τουλάχιστον 5 λιγότερες συμμετοχές από τον top performer:\n")
    print("ID | Stage Name | Festival Count")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")
else:
    print("Δεν βρέθηκαν καλλιτέχνες με 5 λιγότερες συμμετοχές.")

print(f"\nQuery executed in {execution_time:.4f} seconds.")

cursor.close()
conn.close()
