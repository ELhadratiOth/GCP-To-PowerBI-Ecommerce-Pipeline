# Custom Columns & Measures Documentation

## 📋 Custom Columns Created

### 1. Review Score Rating (FACT_ORDERS)

**Purpose**: Categorize review scores into star ratings for visualization

**DAX Formula**:

```DAX
Review Score Rating =
SWITCH(
    INT(FACT_ORDERS[avg_review_score]),
    5, "5 - Excellent",
    4, "4 - Good",
    3, "3 - Average",
    2, "2 - Poor",
    1, "1 - Very Poor",
    "No Rating"
)
```

**Data Type**: Text  

---

### 2. City_State (DIM_CUSTOMERS)

**Purpose**: Combine customer city and state for map visualization

**DAX Formula**:

```DAX
City_State = DIM_CUSTOMERS[customer_city] & ", " & DIM_CUSTOMERS[customer_state]
```

**Data Type**: Text  
**Example Output**: São Paulo, SP | Rio de Janeiro, RJ  

---

## 📊 Measures Created

### Orders & Transactions

#### 1. Total Orders

```DAX
Total Orders = DISTINCTCOUNT(FACT_ORDERS[order_id])
```

---

#### 2. Total Order Items

```DAX
Total Order Items = COUNTROWS(FACT_ORDERS)
```

---

#### 3. Delivered Orders

```DAX
Delivered Orders = CALCULATE(
    DISTINCTCOUNT(FACT_ORDERS[order_id]),
    FACT_ORDERS[is_delivered] = 1
)
```

---

### Revenue & Financial

#### 1. Total Revenue

```DAX
Total Revenue = SUM(FACT_ORDERS[total_payment_value])
```
---

#### 2. Total Cost

```DAX
Total Cost = SUM(FACT_ORDERS[total_item_amount])
```
---

#### 3. Total Profit

```DAX
Total Profit = SUM(FACT_ORDERS[profit])
```
---

#### 4. Profit Margin %

```DAX
Profit Margin % =
DIVIDE(
    SUM(FACT_ORDERS[profit]),
    SUM(FACT_ORDERS[total_payment_value]),
    0
)
```
---

#### 5. Freight Cost

```DAX
Freight Cost = SUM(FACT_ORDERS[item_freight_value])
```
---

### Customer Metrics

#### 1. Total Customers

```DAX
Total Customers = DISTINCTCOUNT(DIM_CUSTOMERS[customer_unique_id])
```
---

### Product & Seller Metrics

#### 1. Total Sellers

```DAX
Total Sellers = DISTINCTCOUNT(FACT_ORDERS[seller_id])
```
---

#### 2. Total Products

```DAX
Total Products = DISTINCTCOUNT(FACT_ORDERS[product_id])
```
---

#### 3. Average Review Score

```DAX
Average Review Score = AVERAGE(FACT_ORDERS[avg_review_score])
```
---

### Delivery Metrics

#### 1. Average Delivery Days

```DAX
Average Delivery Days = AVERAGE(FACT_ORDERS[delivery_days])
```
---

#### 2. Orders Not Yet Delivered

```DAX
Orders Not Yet Delivered =
CALCULATE(
    DISTINCTCOUNT(FACT_ORDERS[order_id]),
    FACT_ORDERS[is_delivered] = 0
)
```
---

#### 3. On-Time Delivery Count

```DAX
On-Time Delivery Count =
SUM(FACT_ORDERS[is_on_time])
```
---

### Payment Metrics

#### 1. Total Payment Value

```DAX
Total Payment Value = SUM(FACT_ORDERS[total_payment_value])
```
---
