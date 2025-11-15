-- METADATA TABLE 
CREATE TABLE IF NOT EXISTS workspace.google_cloud_postgres_public.pipeline_checkpoint (
    table_name STRING,
    last_sync_timestamp TIMESTAMP,
    last_run_time TIMESTAMP,
    rows_processed INT,
    status STRING
)
USING DELTA;



DROP TABLE IF EXISTS workspace.staging.stg_product_category_translation;