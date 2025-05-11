import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

query = """
WITH SubgenreAppearances AS (
    SELECT 
        sg.ID AS Subgenre_ID,
        sg.Name AS Subgenre_Name,
        f.Year,
        COUNT(*) AS Appearance_Count
    FROM Subgenre sg
    JOIN Performer_Subgenre ps ON sg.ID = ps.Subgenre_ID
    JOIN Performer p ON ps.Performer_ID = p.ID
    JOIN Performance pf ON pf.Performer_ID = p.ID
    JOIN Event e ON pf.Event_ID = e.ID
    JOIN Festival f ON e.Festival_ID = f.ID
    GROUP BY sg.ID, f.Year
    HAVING COUNT(*) >= 3
),
ConsecutiveYearPairs AS (
    SELECT 
        s1.Subgenre_ID,
        s1.Subgenre_Name,
        s1.Year AS Year1,
        s2.Year AS Year2,
        s1.Appearance_Count
    FROM SubgenreAppearances s1
    JOIN SubgenreAppearances s2 
      ON s1.Subgenre_ID = s2.Subgenre_ID 
     AND s2.Year = s1.Year + 1
     AND s1.Appearance_Count = s2.Appearance_Count
)
SELECT * FROM ConsecutiveYearPairs
ORDER BY Subgenre_Name, Year1;
"""

cursor.execute(query)
rows = cursor.fetchall()

if rows:
    print("Μουσικά είδη με ίδιο αριθμό εμφανίσεων σε δύο συνεχόμενες χρονιές (≥3):\n")
    print("Subgenre | Έτος 1 | Έτος 2 | Εμφανίσεις")
    print("-" * 50)
    for row in rows:
        print(f"{row[1]} | {row[2]} | {row[3]} | {row[4]}")
else:
    print("Δεν βρέθηκαν υποείδη με ίδιο αριθμό εμφανίσεων σε δύο συνεχόμενα έτη με τουλάχιστον 3 εμφανίσεις.")

cursor.close()
conn.close()
