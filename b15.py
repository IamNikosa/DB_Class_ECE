import mysql.connector

# --- DB Connection ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

query = """
SELECT 
    v.First_Name,
    v.Last_Name,
    pe.Stage_Name,
    SUM(r.Overall) AS Total_Score
FROM Review r
JOIN Ticket t ON r.Ticket_ID = t.ID
JOIN Spectator sp ON sp.Ticket_ID = t.ID
JOIN Visitor v ON v.ID = sp.Visitor_ID
JOIN Event e ON t.Event_ID = e.ID
JOIN Performance p ON e.ID = p.Event_ID
JOIN Performer pe ON pe.ID = p.Performer_ID
WHERE t.Activated = TRUE
GROUP BY v.ID, pe.ID
ORDER BY Total_Score DESC
LIMIT 5;
"""

cursor.execute(query)
rows = cursor.fetchall()

if rows:
    print("Top-5 επισκέπτες με τη μεγαλύτερη συνολική βαθμολογία σε καλλιτέχνη:\n")
    print("Επισκέπτης | Καλλιτέχνης | Σύνολο Βαθμολογίας")
    print("-" * 50)
    for row in rows:
        full_name = f"{row[0]} {row[1]}"
        print(f"{full_name} | {row[2]} | {row[3]}")
else:
    print("Δεν βρέθηκαν επισκέπτες με αξιολογήσεις.")

cursor.close()
conn.close()
