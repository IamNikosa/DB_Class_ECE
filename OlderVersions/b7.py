import mysql.connector

# --- DB Connection ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

# --- SQL Query ---
query = """
SELECT 
    f.ID AS Festival_ID,
    f.Name AS Festival_Name,
    AVG(
        CASE s.Type
            WHEN 'Trainee' THEN 1
            WHEN 'Beginner' THEN 2
            WHEN 'Intermediate' THEN 3
            WHEN 'Experienced' THEN 4
            WHEN 'Very Experienced' THEN 5
        END
    ) AS Avg_Experience_Level
FROM Festival f
JOIN Event e ON f.ID = e.Festival_ID
JOIN event_staff es ON es.Event_ID = e.ID
JOIN Technical_Staff ts ON es.Staff_ID = ts.Staff_ID
JOIN Staff s ON ts.Staff_ID = s.ID
GROUP BY f.ID
ORDER BY Avg_Experience_Level ASC
LIMIT 1;
"""

# --- Execute & Fetch ---
cursor.execute(query)
row = cursor.fetchone()

if row:
    print("Festival with the lowest average experience level (Technical Staff):")
    print(f"Festival ID: {row[0]}")
    print(f"Festival Name: {row[1]}")
    print(f"Avg Technical Staff Experience: {round(row[2], 2)}")
else:
    print("No technical staff data found.")

# --- Cleanup ---
cursor.close()
conn.close()
