# Bus Trip Data Pipeline

A production-ready pipeline for ingesting, processing, and analyzing NSW Bus Trip data using Apache Iceberg, Trino, SQLMesh, and Snowflake.

---

## 🚀 Overview

This project fetches NSW bus trip data, stores it in S3 using Iceberg tables, and enables analytics via Trino and SQLMesh. It supports scalable ingestion, transformation, and querying for both raw and curated datasets.

---

## 📁 Project Structure

```
.
├── ingestion/                # Data fetching and export scripts
│   ├── fetch_bus_trips.py    # Fetches data from NSW API
│   └── export_to_iceberg.py  # Loads data into Iceberg via Trino
├── models/                   # SQLMesh models (raw & curated)
│   ├── raw/
│   │   └── raw_bus_trip_counts_filtered.sql
│   └── curated/
│       └── bus_trip_summary.sql
├── tests/                    # SQLMesh test queries
│   └── test_no_negative_trips_filtered.sql
├── trino/                    # Trino configuration
│   ├── etc/
│   └── catalog/
├── config.yaml               # SQLMesh configuration
├── docker-compose.yaml       # Trino deployment
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
└── README.md                 # Project documentation
```

---

## ⚙️ Prerequisites

- Docker & Docker Compose
- AWS Account with S3 access
- Python 3.8+
- SQLMesh CLI
- Snowflake Account

---

## 🏁 Quick Start

### 1. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=ap-southeast-2
S3_BUCKET_NAME=your_bucket_name_here
NSW_API_TOKEN=your_api_token_here
# ... Snowflake variables if needed
```

### 2. Install Python Dependencies

```sh
pip install -r requirements.txt
```

### 3. Start Trino

```sh
docker-compose up -d
```

### 4. Run Data Ingestion

```sh
python ingestion/export_to_iceberg.py
```

### 5. Initialize SQLMesh

```sh
sqlmesh plan
sqlmesh run
```

---

## 🗄️ Data Flow

1. **Fetch Data:** [`ingestion/fetch_bus_trips.py`](ingestion/fetch_bus_trips.py) pulls data from the NSW API.
2. **Export to Iceberg:** [`ingestion/export_to_iceberg.py`](ingestion/export_to_iceberg.py) writes data to S3 and loads it into Iceberg tables via Trino.
3. **Modeling:** SQLMesh models in [`models/raw/raw_bus_trip_counts_filtered.sql`](models/raw/raw_bus_trip_counts_filtered.sql) and [`models/curated/bus_trip_summary.sql`](models/curated/bus_trip_summary.sql) transform and aggregate the data.
4. **Testing:** SQLMesh tests in [`tests/test_no_negative_trips_filtered.sql`](tests/test_no_negative_trips_filtered.sql) validate data quality.

---

## 🧩 Configuration

- **Trino:** Configured in [`trino/etc/`](trino/etc/) and [`trino/catalog/`](trino/catalog/).
- **SQLMesh:** Gateway and model defaults in [`config.yaml`](config.yaml).
- **Docker Compose:** Trino deployment in [`docker-compose.yaml`](docker-compose.yaml).

---

## 🧪 Testing

Run SQLMesh tests:

```sh
sqlmesh test
```

---

## 📚 Resources

- [Apache Iceberg Documentation](https://iceberg.apache.org/docs/latest/)
- [Trino Documentation](https://trino.io/docs/current/)
- [SQLMesh Documentation](https://sqlmesh.readthedocs.io/)