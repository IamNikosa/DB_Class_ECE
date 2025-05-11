import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

query = """
WITH GenreAppearances AS (
    SELECT 
        g.ID AS Genre_ID,
        g.Name AS Genre_Name,
        f.Year,
        COUNT(*) AS Appearance_Count
    FROM Genre g
    JOIN Subgenre sg ON sg.Genre_ID = g.ID
    JOIN Performer_Subgenre ps ON sg.ID = ps.Subgenre_ID
    JOIN Performance pf ON pf.Performer_ID = ps.Performer_ID
    JOIN Event e ON pf.Event_ID = e.ID
    JOIN Festival f ON e.Festival_ID = f.ID
    GROUP BY g.ID, f.Year
    HAVING COUNT(*) >= 3
),
ConsecutiveYearPairs AS (
    SELECT 
        g1.Genre_ID,
        g1.Genre_Name,
        g1.Year AS Year1,
        g2.Year AS Year2,
        g1.Appearance_Count
    FROM GenreAppearances g1
    JOIN GenreAppearances g2 
      ON g1.Genre_ID = g2.Genre_ID
     AND g2.Year = g1.Year + 1
     AND g1.Appearance_Count = g2.Appearance_Count
)
SELECT * FROM ConsecutiveYearPairs
ORDER BY Genre_Name, Year1;
"""

cursor.execute(query)
rows = cursor.fetchall()

if rows:
    print("Μουσικά είδη με ίδιο αριθμό εμφανίσεων σε δύο συνεχόμενες χρονιές (≥3):\n")
    print("Genre | Έτος 1 | Έτος 2 | Εμφανίσεις")
    print("-" * 50)
    for row in rows:
        print(f"{row[1]} | {row[2]} | {row[3]} | {row[4]}")
else:
    print("Δεν βρέθηκαν είδη με ίδιο αριθμό εμφανίσεων σε δύο συνεχόμενα έτη με τουλάχιστον 3 εμφανίσεις.")

cursor.close()
conn.close()
