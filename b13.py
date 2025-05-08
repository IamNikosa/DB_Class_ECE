import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

query = """
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    COUNT(DISTINCT l.Continent) AS Continents_Performed
FROM Performer pe
JOIN Performance p ON pe.ID = p.Performer_ID
JOIN Event e ON p.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
JOIN Location l ON f.Location_ID = l.ID
GROUP BY pe.ID
HAVING COUNT(DISTINCT l.Continent) >= 3
ORDER BY Continents_Performed DESC;
"""

cursor.execute(query)
rows = cursor.fetchall()

if rows:
    print("Καλλιτέχνες με συμμετοχές σε τουλάχιστον 3 διαφορετικές ηπείρους:\n")
    print("ID | Stage Name | Ήπειροι")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")
else:
    print("Δεν βρέθηκαν καλλιτέχνες με συμμετοχές σε 3 ή περισσότερες ηπείρους.")

cursor.close()
conn.close()
