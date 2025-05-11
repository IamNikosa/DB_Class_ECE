import mysql.connector
import time
start_time=time.time()

# --- Connect to the database ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='xaua6709ni!',
    database='Festival'
)
cursor = conn.cursor()

# --- Updated SQL query with extra names ---
query = """
SELECT 
    p.Performer_ID,
    pe.Real_Name,
    pe.Stage_Name,
    f.ID AS Festival_ID,
    f.Name AS Festival_Name,
    COUNT(*) AS WarmUp_Count
FROM Performance p
JOIN Event e ON p.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
JOIN Performer pe ON p.Performer_ID = pe.ID
WHERE p.Type = 'Warm up'
GROUP BY p.Performer_ID, f.ID
HAVING COUNT(*) > 2;
"""

# --- Execute query and print column names + rows ---
cursor.execute(query)
columns = [desc[0] for desc in cursor.description]

end_time = time.time()
execution_time = end_time - start_time


print(" | ".join(columns))

for row in cursor.fetchall():
    print(" | ".join(str(col) if col is not None else "NULL" for col in row))

print(f"\nQuery executed in {execution_time:.4f} seconds.")

# --- Cleanup ---
cursor.close()
conn.close()
