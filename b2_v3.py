import mysql.connector

# --- User Input ---
target_genre = 'Indie'
target_year = 2024

# --- Connect ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

# --- SQL ---
query = """
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    IF(COUNT(pf.ID) > 0, 'YES', 'NO') AS Participated
FROM Genre g
JOIN Subgenre sg ON sg.Genre_ID = g.ID
JOIN Performer_Subgenre ps ON ps.Subgenre_ID = sg.ID
JOIN Performer pe ON ps.Performer_ID = pe.ID
LEFT JOIN Performance pf ON pf.Performer_ID = pe.ID
LEFT JOIN Event e ON pf.Event_ID = e.ID
LEFT JOIN Festival f ON e.Festival_ID = f.ID AND f.Year = %s
WHERE g.Name = %s
GROUP BY pe.ID;
"""

cursor.execute(query, (target_year, target_genre))
rows = cursor.fetchall()

# --- Output ---
if rows:
    print(f"Καλλιτέχνες του είδους '{target_genre}' και συμμετοχή στο έτος {target_year}:\n")
    print("ID | Stage Name       | Participated")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]} | {row[1]:<17} | {row[2]}")
else:
    print("Δεν βρέθηκαν καλλιτέχνες για αυτό το είδος ή δεν υπάρχουν συμμετοχές.")

cursor.close()
conn.close()
