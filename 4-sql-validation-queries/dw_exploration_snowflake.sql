SHOW TABLES;


-- Check table row counts
SELECT
  'FACT_ORDERS' as table_name, COUNT(*) as row_count FROM FACT_ORDERS
UNION ALL
SELECT 'DIM_CUSTOMERS', COUNT(*) FROM DIM_CUSTOMERS
UNION ALL
SELECT 'DIM_SELLERS', COUNT(*) FROM DIM_SELLERS
UNION ALL
SELECT 'DIM_PRODUCTS', COUNT(*) FROM DIM_PRODUCTS
UNION ALL
SELECT 'DIM_DATE', COUNT(*) FROM DIM_DATE
ORDER BY row_count DESC;


-- Count null values in each column
SELECT
  COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as null_customer_id,
  COUNT(CASE WHEN seller_id IS NULL THEN 1 END) as null_seller_id,
  COUNT(CASE WHEN product_id IS NULL THEN 1 END) as null_product_id,
  COUNT(CASE WHEN total_payment_value IS NULL THEN 1 END) as null_payment_value,
  COUNT(CASE WHEN avg_review_score IS NULL THEN 1 END) as null_review_score
FROM FACT_ORDERS;

-- View sample fact orders with dimension details
SELECT
  f.order_id,
  f.order_item_id,
  c.customer_city,
  c.customer_state,
  s.seller_city,
  s.seller_state,
  p.product_category_name_english,
  f.item_price,
  f.item_freight_value,
  f.total_item_amount,
  f.total_payment_value,
  f.avg_review_score,
  f.order_status,
  f.delivery_delay_flag,
  d.day_name,
  d.month_name,
  d.year
FROM FACT_ORDERS f
LEFT JOIN DIM_CUSTOMERS c ON f.customer_id = c.customer_id
LEFT JOIN DIM_SELLERS s ON f.seller_id = s.seller_id
LEFT JOIN DIM_PRODUCTS p ON f.product_id = p.product_id
LEFT JOIN DIM_DATE d ON f.order_purchase_date_id = d.date_id
LIMIT 10;


-- Total Revenue by Month

SELECT
  d.year,
  d.month,
  d.month_name,
  COUNT(DISTINCT f.order_id) as total_orders,
  COUNT(*) as total_items,
  ROUND(SUM(f.total_payment_value), 2) as total_revenue,
  ROUND(AVG(f.total_payment_value), 2) as avg_order_value,
  ROUND(SUM(f.profit), 2) as total_profit
FROM FACT_ORDERS f
LEFT JOIN DIM_DATE d ON f.order_purchase_date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year DESC, d.month DESC;

-- Total Customers & Order Statistics

SELECT
  COUNT(DISTINCT c.customer_unique_id) as total_unique_customers,
  COUNT(DISTINCT f.order_id) as total_orders,
  ROUND(COUNT(DISTINCT f.order_id) / COUNT(DISTINCT c.customer_unique_id), 2) as avg_orders_per_customer,
  ROUND(SUM(f.total_payment_value) / COUNT(DISTINCT c.customer_unique_id), 2) as avg_customer_lifetime_value,
  ROUND(AVG(f.total_payment_value), 2) as avg_order_value,
  ROUND(MIN(f.total_payment_value), 2) as min_order_value,
  ROUND(MAX(f.total_payment_value), 2) as max_order_value
FROM FACT_ORDERS f
LEFT JOIN DIM_CUSTOMERS c ON f.customer_id = c.customer_id;

-- Most Reviewed Products

SELECT
  p.product_id,
  p.product_category_name_english,
  COUNT(DISTINCT f.order_id) as times_purchased,
  SUM(f.total_reviews) as total_reviews,
  ROUND(AVG(f.avg_review_score), 2) as avg_rating,
  ROUND(SUM(f.total_payment_value), 2) as total_revenue,
  ROUND(AVG(f.total_payment_value), 2) as avg_price
FROM FACT_ORDERS f
LEFT JOIN DIM_PRODUCTS p ON f.product_id = p.product_id
WHERE p.product_id IS NOT NULL AND f.total_reviews > 0
GROUP BY p.product_id, p.product_category_name_english
ORDER BY total_reviews DESC
LIMIT 10;

-- Revenue by Customer Location

SELECT
  c.customer_state,
  c.customer_city,
  COUNT(DISTINCT f.order_id) as orders,
  ROUND(SUM(f.total_payment_value), 2) as revenue,
  ROUND(AVG(f.total_payment_value), 2) as avg_order_value,
  ROUND(AVG(f.avg_review_score), 2) as avg_rating
FROM FACT_ORDERS f
LEFT JOIN DIM_CUSTOMERS c ON f.customer_id = c.customer_id
WHERE c.customer_state IS NOT NULL
GROUP BY c.customer_state, c.customer_city
ORDER BY revenue DESC;
