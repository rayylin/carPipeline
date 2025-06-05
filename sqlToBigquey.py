import os
from google.cloud import bigquery
import pandas as pd
from config import eid, pathBigQuery, conn
import decimal

cursor = conn.cursor()

# Set path to your JSON key file

os.environ[eid] = pathBigQuery

# Initialize BigQuery client
client = bigquery.Client()


# Step 1: Get latest date from BigQuery
query = "SELECT MAX(date) as max_date FROM `carpipe.stockPrice.stockPrice`"
latest_date = client.query(query).result().to_dataframe().iloc[0]['max_date']

print(latest_date)


# Step 2: Query SQL Server
query_sql = "SELECT * FROM [financeDb].[dbo].[stock] WHERE [date] > ? "
cursor.execute(query_sql, latest_date)
rows = cursor.fetchall()

# Convert to DataFrame
columns = [column[0] for column in cursor.description]
df_new = pd.DataFrame.from_records(rows, columns=columns)


# Step 3: Upload new data to BigQuery


# Sanitize DataFrame for BigQuery
for col in df_new.columns:
    if df_new[col].apply(lambda x: isinstance(x, decimal.Decimal)).any():
        df_new[col] = df_new[col].astype(float)

# Load to BigQuery
client.load_table_from_dataframe(
    df_new,
    "carpipe.stockPrice.stockPrice"
).result()