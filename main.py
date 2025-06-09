
def transfer_stock_data(request):
    import os
    from google.cloud import bigquery
    import pandas as pd
    from config import eid, pathBigQuery, conn
    import decimal
    #import pyodbc

    cursor = conn.cursor()

    # Set path to your JSON key file
    os.environ[eid] = pathBigQuery

    # Initialize BigQuery client
    client = bigquery.Client()


    # Step 1: Get latest date from BigQuery
    query = "SELECT MAX(date) as max_date FROM `ccarpipe.car_data.car`"
    latest_date = client.query(query).result().to_dataframe().iloc[0]['max_date']

    print(latest_date)


    # Step 2: Query SQL Server
    query_sql = "SELECT * FROM [testdb1].[dbo].[Cars] WHERE [date] > ? "
    cursor.execute(query_sql, latest_date)
    rows = cursor.fetchall()

    # Convert to DataFrame
    columns = [column[0] for column in cursor.description]
    df_new = pd.DataFrame.from_records(rows, columns=columns)


    # Sanitize DataFrame for BigQuery
    for col in df_new.columns:
        if df_new[col].apply(lambda x: isinstance(x, decimal.Decimal)).any():
            df_new[col] = df_new[col].astype(float)

    # Load to BigQuery
    client.load_table_from_dataframe(
        df_new,
        "carpipe.stockPrice.stockPrice"
    ).result()


    return "Transfer complete", 200


def hello_world(request):
    return "Hello, World!", 200