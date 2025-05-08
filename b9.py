import mysql.connector

# --- Connect to DB ---
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
    Year,
    View_Count,
    GROUP_CONCAT(Visitor_ID) AS Visitors
FROM (
    SELECT 
        sp.Visitor_ID,
        f.Year,
        COUNT(DISTINCT e.ID) AS View_Count
    FROM Spectator sp
    JOIN Ticket t ON sp.Ticket_ID = t.ID
    JOIN Event e ON t.Event_ID = e.ID
    JOIN Festival f ON e.Festival_ID = f.ID
    GROUP BY sp.Visitor_ID, f.Year
    HAVING View_Count > 3
) AS yearly_counts
GROUP BY Year, View_Count
HAVING COUNT(*) > 1;
"""

# --- Execute and fetch ---
cursor.execute(query)
rows = cursor.fetchall()

# --- Print results ---
if rows:
    print("Έτη και αριθμοί παραστάσεων με κοινούς επισκέπτες (>3):\n")
    print("Έτος | Παραστάσεις | Επισκέπτες")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]} | {row[1]} παραστάσεις | Επισκέπτες: {row[2]}")
else:
    print("Δεν βρέθηκαν επισκέπτες με ίδιο πλήθος παραστάσεων >3 μέσα στο ίδιο έτος.")

# --- Cleanup ---
cursor.close()
conn.close()
