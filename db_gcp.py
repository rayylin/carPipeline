# test connect to gcp
import pyodbc

from config import conn
from sqlScript import insertStock, selectStock

cursor = conn.cursor()

#cursor.execute(insertStock, ('AAPL', '2025-11-05', 198.53, 198.53, 198.53, 198.53))

cursor.execute()

# conn.commit()
cursor.execute(selectStock)

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()