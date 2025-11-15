-- Retrieve all column names from the "customers_table"
SELECT
  "column_name"
FROM
  information_schema.columns
WHERE
  table_name = 'customers_table';

-- Display the first 4 rows from the "customers_table" for a quick preview
SELECT
  *
FROM
  customers_table
LIMIT 4;

-- Count the number of unique customer IDs 
-- Result: 99,441 distinct customer_id values
SELECT
  COUNT(DISTINCT "customer_id")
FROM
  "customers_table";

-- Count the number of unique customers based on "customer_unique_id"
-- This gives the real number of individual customers ( instead of using there names for exmple )
-- Result: 96,096 distinct customer_unique_id values
SELECT
  COUNT(DISTINCT "customer_unique_id")
FROM
  "customers_table";

















