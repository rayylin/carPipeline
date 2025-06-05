# test connect to gcp
import pyodbc

from config import conn
from sqlScript import insertStock, selectStock

cursor = conn.cursor()


# SELECT TOP (1000) [car_ID]
#       ,[symboling]
#       ,[CarName]
#       ,[fueltype]
#       ,[aspiration]
#       ,[doornumber]
#       ,[carbody]
#       ,[drivewheel]
#       ,[enginelocation]
#       ,[wheelbase]
#       ,[carlength]
#       ,[carwidth]
#       ,[carheight]
#       ,[curbweight]
#       ,[enginetype]
#       ,[cylindernumber]
#       ,[enginesize]
#       ,[fuelsystem]
#       ,[boreratio]
#       ,[stroke]
#       ,[compressionratio]
#       ,[horsepower]
#       ,[peakrpm]
#       ,[citympg]
#       ,[highwaympg]
#       ,[price]
#   FROM [testdb1].[dbo].[Cars]




cursor.execute("select top (12) * from [testdb1].[dbo].[Cars]")

# conn.commit()
# cursor.execute(selectStock)

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()