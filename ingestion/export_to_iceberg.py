import os
import tempfile
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
from trino.dbapi import connect
from dotenv import load_dotenv
from datetime import datetime
from fetch_bus_trips import fetch_bus_data

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

ICEBERG_DB = "bus_trip_db"
ICEBERG_TABLE = "raw_bus_trip_counts"
ICEBERG_FULL_NAME = f"{ICEBERG_DB}.{ICEBERG_TABLE}"
S3_BASE_PATH = f"s3://{S3_BUCKET}/bus_trips/raw"

TRINO_HOST = "localhost"
TRINO_PORT = 8080
TRINO_USER = "trino"
TRINO_CATALOG = "iceberg"

def ensure_iceberg_table():
    conn = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=TRINO_USER,
        catalog=TRINO_CATALOG,
        schema=ICEBERG_DB
    )
    cur = conn.cursor()
 
    # Create schema and table if needed
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {ICEBERG_DB} WITH (location = '{S3_BASE_PATH}/')")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {ICEBERG_FULL_NAME} (
            id VARCHAR,
            year_month VARCHAR,
            bus_region VARCHAR,
            card_type VARCHAR,
            trips INTEGER
        )
        WITH (
            format = 'PARQUET',
            partitioning = ARRAY['year_month']
        )
    """)


    print(f"Iceberg table ensured: {ICEBERG_FULL_NAME}")

def write_parquet(df, year_month):
    local_dir = tempfile.mkdtemp()
    filename = f"bus_trips_{year_month}.parquet"
    file_path = os.path.join(local_dir, filename)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)
    return file_path, filename

def upload_to_s3(local_path, year_month, filename):
    s3_key = f"bus_trips/raw/year_month={year_month}/{filename}"
    s3 = boto3.client("s3", region_name=REGION)
    s3.upload_file(local_path, S3_BUCKET, s3_key)
    print(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")
    return f"{S3_BASE_PATH}/year_month={year_month}/{filename}"

def insert_into_iceberg(df):
    # take only first 100 rows of the dataframe
    df = df.head(10)
    print("Inserting rows into Iceberg table via Trino...")
    conn = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=TRINO_USER,
        catalog=TRINO_CATALOG,
        schema=ICEBERG_DB
    )
    cur = conn.cursor()

    for _, row in df.iterrows():
        insert_sql = f"""
            INSERT INTO {ICEBERG_TABLE} (
                id, year_month, bus_region, card_type, trips
            ) VALUES (
                '{row["id"]}',
                '{row["year_month"]}',
                '{row["bus_region"]}',
                '{row["card_type"]}',
                {int(row["trips"])}
            )
        """
        cur.execute(insert_sql)

    print(f"Inserted {len(df)} rows into {ICEBERG_FULL_NAME}")

def main():
    df = fetch_bus_data()
    if df.empty:
        return

    year_month = df["year_month"].iloc[0]
    ensure_iceberg_table()
    insert_into_iceberg(df)

    print("\n Done. Data exported to Iceberg.\n")
    print(f"→ Trino query: SELECT * FROM {ICEBERG_FULL_NAME} LIMIT 10;")

if __name__ == "__main__":
    main()
