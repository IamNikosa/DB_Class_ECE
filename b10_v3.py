import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

query = """
SELECT 
    LEAST(g1.Name, g2.Name) AS Genre1,
    GREATEST(g1.Name, g2.Name) AS Genre2,
    COUNT(DISTINCT f.ID) AS Festival_Count
FROM Performer_Subgenre ps1
JOIN Subgenre sg1 ON ps1.Subgenre_ID = sg1.ID
JOIN Genre g1 ON sg1.Genre_ID = g1.ID

JOIN Performer_Subgenre ps2 
    ON ps1.Performer_ID = ps2.Performer_ID
    AND ps1.Subgenre_ID < ps2.Subgenre_ID
JOIN Subgenre sg2 ON ps2.Subgenre_ID = sg2.ID
JOIN Genre g2 ON sg2.Genre_ID = g2.ID

JOIN Performance p ON ps1.Performer_ID = p.Performer_ID
JOIN Event e ON p.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID

WHERE g1.ID <> g2.ID
GROUP BY Genre1, Genre2
ORDER BY Festival_Count DESC
LIMIT 3;
"""

cursor.execute(query)
rows = cursor.fetchall()

if rows:
    print("Top-3 ζεύγη μουσικών υποειδών που εμφανίστηκαν σε φεστιβάλ:\n")
    print("Είδος 1 | Είδος 2 | Φεστιβάλ")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")
else:
    print("Δεν βρέθηκαν κοινά ζεύγη υποειδών.")

cursor.close()
conn.close()
