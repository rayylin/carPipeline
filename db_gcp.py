# test connect to gcp
import pyodbc

from config import conn
from sqlScript import insertStock

cursor = conn.cursor()

cursor.execute(insertStock, ('AAPL', '2025-11-05', 198.53, 198.53, 198.53, 198.53))

# conn.commit()
cursor.execute("SELECT * FROM stock")

for row in cursor.fetchall():
    print(row)
    print("create done")

cursor.close()
conn.close()