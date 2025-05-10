import mysql.connector

# --- Connect to the database ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Festival'
)
cursor = conn.cursor()

# --- Query to calculate revenue per year per payment method ---
query ="""
SELECT 
    f.Year,
    COALESCE(p.Name, 'ΣΥΝΟΛΟ') AS Τρόπος_Πληρωμής,
    SUM(t.Price) AS Έσοδα
FROM Transaction tr
JOIN Ticket t ON tr.Ticket_ID = t.ID
JOIN Event e ON t.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
JOIN Type tp ON t.Type_ID = tp.Name
LEFT JOIN Payment p ON tr.Payment_ID = p.Name
WHERE tr.Is_Resale = FALSE
GROUP BY f.Year, p.Name;
"""

# --- Execute and fetch ---
cursor.execute(query)
rows = cursor.fetchall()

# --- Print results ---
print("Έτος | Τρόπος Πληρωμής | Έσοδα (€)")
print("---------------------------------------")
for row in rows:
    year, payment_method, revenue = row
    print(f"{year:<5} | {payment_method:<18} | {revenue:.2f}")

# --- Cleanup ---
cursor.close()
conn.close()
