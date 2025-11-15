# Data Ingestion Cloud Function

A GCP Cloud Function that automates the ingestion of the Brazilian ecommerce dataset from Kaggle into a PostgreSQL database in Google Cloud SQL.

## Overview

This Cloud Function performs the following tasks:

1. **Downloads dataset from Kaggle** - Retrieves the `olistbr/brazilian-ecommerce` dataset using the kagglehub library
2. **Discovers CSV files** - Scans the downloaded dataset for all CSV files
3. **Drops existing tables** - Removes all existing tables from the database before ingestion
4. **Creates tables dynamically** - Creates a new table for each CSV file with all columns as TEXT type
5. **Inserts data in batches** - Loads data from CSV files in batches of 100 rows for efficiency
6. **Handles special characters** - Properly escapes single quotes in data to prevent SQL injection
7. **Supports encoding fallback** - Handles UTF-8 and latin1 character encodings

## Features

- **HTTP-triggered function** - Accessible via HTTP requests
- **Environment-based configuration** - Database credentials via environment variables
- **Automatic table naming** - Removes `olist_` prefix and `_dataset` suffix, adds `_table` suffix
- **Error handling** - Returns detailed error messages on failure
- **Health check endpoint** - Provides container health verification
- **Raw data ingestion** - Stores unprocessed CSV data as-is
 - **Raw data ingestion** - Stores unprocessed CSV data as-is
 - **Idempotent ingestion** - Each ingestion run drops existing tables before creating and inserting new ones; repeated runs are safe and will replace previous data
 - **Cloud SQL compatible** - Connects via Unix socket to Google Cloud SQL Proxy

## Table Naming Convention

CSV files are transformed to table names as follows:

```
olist_order_payments_dataset.csv → order_payments_table
olist_customers_dataset.csv      → customers_table
olist_orders_dataset.csv         → orders_table
olist_order_reviews_dataset.csv  → order_reviews_table
```

## Setup

### Prerequisites

- GCP project with Cloud Functions enabled
- Google Cloud SQL PostgreSQL instance
- Kaggle API credentials configured in the environment

### Environment Variables

Configure these environment variables for your Cloud Function:

```bash
DB_HOST=/cloudsql/PROJECT:REGION:INSTANCE  # Cloud SQL Proxy socket path
DB_NAME=your_database_name                 # PostgreSQL database name
DB_USER=postgres                           # PostgreSQL username
DB_PASSWORD=your_password                  # PostgreSQL password
```

## Dependencies

- `functions-framework==3.5.0` - GCP Cloud Functions framework
- `kagglehub==0.2.8` - Kaggle dataset download library
- `pandas==2.2.0` - Data processing and CSV reading
- `sqlalchemy==2.1.0` - Database ORM and connection management
- `psycopg2-binary==2.10.1` - PostgreSQL database adapter

## Usage

### Trigger the ingestion

```bash
curl -X POST https://REGION-PROJECT_ID.cloudfunctions.net/ingest_data
```

### Response Format

**Success response (HTTP 200):**

```json
{
  "status": "success",
  "message": "Data stored successfully",
  "total_rows": 12345,
  "tables": [
    {
      "table": "order_payments_table",
      "rows": 1000,
      "columns": ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"]
    },
    {
      "table": "customers_table",
      "rows": 2000,
      "columns": ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"]
    }
  ]
}
```

**Error response (HTTP 400/500):**

```json
{
  "status": "error",
  "message": "Database connection failed: ...",
  "details": "Traceback details (if applicable)"
}
```

## Function Endpoint

### `ingest_data(request)`

Main HTTP endpoint that performs the complete data ingestion workflow.

- **Trigger:** HTTP POST/GET
- **Authentication:** Requires valid Kaggle credentials
- **Timeout:** 900 seconds
- **Memory:** 4GB
- **Returns:** JSON response with status and ingestion details


## How It Works

1. **Connection Setup** - Establishes connection to Cloud SQL via Unix socket
2. **Dataset Download** - Downloads Brazilian ecommerce dataset from Kaggle (uses cache if available)
3. **Table Discovery** - Finds all CSV files in the dataset
4. **Table Cleanup** - Drops all existing tables before ingestion starts
5. **Batch Processing** - For each CSV file:
   - Reads CSV data with pandas
   - Creates empty table with TEXT columns
   - Inserts data in 100-row batches using raw SQL
   - Handles special characters and encoding issues
6. **Response** - Returns summary of created tables and row counts

## Data Handling

- **All columns are TEXT type** - No type conversion is performed
- **NULL values** - Empty cells in CSV are stored as SQL NULL
- **Special characters** - Single quotes are escaped (`'` → `''`)
- **Encoding** - UTF-8 is used by default, with latin1 fallback if needed

## Error Handling

The function includes comprehensive error handling for:

- Missing environment variables
- Database connection failures
- Kaggle dataset download errors
- CSV file reading issues (encoding problems)
- SQL execution errors
- Missing or invalid data

Each error returns a descriptive JSON response with status code and error details.

## Performance

- **Batch size:** 100 rows per INSERT statement (optimized for PostgreSQL)
- **Connection pooling:** Disabled for Cloud SQL Proxy compatibility
- **Caching:** Dataset caching enabled to avoid repeated downloads
- **Typical execution time:** 2-5 minutes depending on dataset size

