import functions_framework
import os
import tempfile
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
import kagglehub

@functions_framework.http
def ingest_data(request):

    try:
        # --- Read DB configuration from environment variables ---
        db_host = os.getenv("DB_HOST") 
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        
        if not all([db_host, db_name, db_user, db_password]):
            return {
                "status": "error",
                "message": "Missing environment variables: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD"
            }, 400
        
        # --- Download Kaggle dataset ---
        dataset_path = kagglehub.dataset_download(
            "olistbr/brazilian-ecommerce",
        )
        
        if not os.path.isdir(dataset_path):
            return {"status": "error", "message": "Dataset path not found"}, 400

        # --- Create PostgreSQL connection ---
        db_url = f"postgresql+psycopg2://{db_user}:{db_password}@/{db_name}?host={db_host}"
        try:
            engine = create_engine(
                db_url,
                connect_args={
                    "connect_timeout": 10,
                    "host": db_host
                },
                poolclass=None,
                echo=False
            )
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except Exception as conn_error:
            return {
                "status": "error",
                "message": f"Database connection failed: {str(conn_error)}"
            }, 400
        
        # --- Find all CSV files ---
        csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
        if not csv_files:
            return {"status": "error", "message": "No CSV files found in dataset"}, 400
        
        tables_created = []
        total_rows = 0
        
        # --- Drop all existing tables before ingestion ---
        with engine.begin() as connection:
            for csv_file in csv_files:
                base_name = csv_file.replace('.csv', '').lower()
                if base_name.startswith('olist_'):
                    base_name = base_name[6:]  # Remove 'olist_' prefix
                if base_name.endswith('_dataset'):
                    base_name = base_name[:-8]  # Remove '_dataset' suffix
                table_name = base_name + '_table'
                try:
                    connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                except Exception:
                    pass 
        
        # --- Process each CSV ---
        for csv_file in csv_files:
            file_path = os.path.join(dataset_path, csv_file)
            # Remove prefix 'olist_' and suffix '_dataset', then add '_table'
            base_name = csv_file.replace('.csv', '').lower()
            if base_name.startswith('olist_'):
                base_name = base_name[6:]  # Remove 'olist_' prefix
            if base_name.endswith('_dataset'):
                base_name = base_name[:-8]  # Remove '_dataset' suffix
            table_name = base_name + '_table'
            
            try:
                # Try reading CSV with UTF-8 first, fallback to latin1
                try:
                    df = pd.read_csv(file_path)
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='latin1')
                
                # Use raw SQL to insert data
                with engine.begin() as connection:
                    # Create table with all columns as TEXT
                    columns_def = ", ".join([f'"{col}" TEXT' for col in df.columns])
                    create_table_sql = f"CREATE TABLE {table_name} ({columns_def})"
                    connection.execute(text(create_table_sql))
                    
                    # Insert data in batches using direct SQL
                    batch_size = 100
                    for i in range(0, len(df), batch_size):
                        batch = df.iloc[i:i+batch_size]
                        
                        col_names = ", ".join([f'"{col}"' for col in df.columns])
                        
                        # Create VALUES clause with proper escaping
                        values_list = []
                        for _, row in batch.iterrows():
                            row_values = []
                            for val in row:
                                if pd.isna(val):
                                    row_values.append("NULL")
                                else:
                                    str_val = str(val).replace("'", "''")
                                    row_values.append(f"'{str_val}'")
                            values_list.append(f"({', '.join(row_values)})")
                        
                        values_clause = ", ".join(values_list)
                        insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES {values_clause}"
                        
                        cursor = connection.connection.cursor()
                        try:
                            cursor.execute(insert_sql)
                        finally:
                            cursor.close()
                
                tables_created.append({
                    "table": table_name,
                    "rows": len(df),
                    "columns": list(df.columns)
                })
                total_rows += len(df)
            
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                return {
                    "status": "error",
                    "message": f"Failed to process {csv_file}: {str(e)}",
                    "details": error_details
                }, 500
        
        engine.dispose()
        
        return {
            "status": "success",
            "message": "Data stored successfully",
            "total_rows": total_rows,
            "tables": tables_created
        }, 200
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed: {str(e)}"
        }, 500
