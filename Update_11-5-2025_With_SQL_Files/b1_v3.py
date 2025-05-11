import mysql.connector
import time
start_time=time.time()

# --- Connect to the database ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='xaua6709ni!',
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
GROUP BY f.Year, p.Name WITH ROLLUP
HAVING NOT (f.Year IS NULL)  -- exclude grand total
"""

# --- Execute and fetch ---
cursor.execute(query)
rows = cursor.fetchall()

end_time = time.time()
execution_time = end_time - start_time

# --- Print results ---
print("Έτος | Τρόπος Πληρωμής | Έσοδα (€)")
print("---------------------------------------")
previous_year = None
for year, payment_method, revenue in rows:
    year_display = f"{year:<6}" if year != previous_year else " " * 6
    print(f"{year_display:<5} | {payment_method:<18} | {revenue:.2f}")
    previous_year = year


print(f"\nQuery executed in {execution_time:.4f} seconds.")


# --- Cleanup ---
cursor.close()
conn.close()
