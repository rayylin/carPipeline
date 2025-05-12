# test connect to gcp
import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=34.58.90.139,1433;'
    'DATABASE=cardb1;'
    'UID=user2;'
    'PWD=12345678;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
    'Connection Timeout=30;'
)

cursor = conn.cursor()

cursor.execute("""CREATE TABLE stock (
                    id NVARCHAR(20),
                    date DATETIME,
                    start NUMERIC(12,4),
                    [end] NUMERIC(12,4),
                    high NUMERIC(12,4),
                    low NUMERIC(12,4)
                    );""")
cursor.execute("""
    INSERT INTO stock (id, date, start, [end], high, low)
    VALUES (?, ?, ?, ?, ?, ?)
""", ('AAPL', '2025-11-05', 198.53, 198.53, 198.53, 198.53))
cursor.execute("SELECT * FROM stock")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()