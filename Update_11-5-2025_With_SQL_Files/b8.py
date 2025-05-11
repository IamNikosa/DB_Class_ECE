import mysql.connector
import time

# --- Connect to the database ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='xaua6709ni!',
    database='Festival'
)
cursor = conn.cursor()

# --- Ask for date input ---
target_date = input("Δώσε ημερομηνία (YYYY-MM-DD): ").strip()

start_time=time.time()

# --- SQL Query ---
query = """
SELECT s.ID, s.Name
FROM Support_Staff ss
JOIN Staff s ON ss.Staff_ID = s.ID
LEFT JOIN event_staff es ON s.ID = es.Staff_ID
LEFT JOIN Event e ON es.Event_ID = e.ID AND DATE(e.Start_Time) = %s
WHERE e.ID IS NULL;
"""

# --- Execute query ---
cursor.execute(query, (target_date,))
rows = cursor.fetchall()

end_time = time.time()
execution_time = end_time - start_time

# --- Display Results ---
if rows:
    print(f"\nΥποστηρικτικό προσωπικό ΧΩΡΙΣ εργασία στις {target_date}:")
    for row in rows:
        print(f"- ID: {row[0]}, Όνομα: {row[1]}")
else:
    print(f"\nΌλο το υποστηρικτικό προσωπικό έχει ανατεθεί σε δουλειά στις {target_date}.")

print(f"\nQuery executed in {execution_time:.4f} seconds.")

# --- Cleanup ---
cursor.close()
conn.close()
