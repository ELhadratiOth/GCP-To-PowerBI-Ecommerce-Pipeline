# Power Query Transformations Documentation

## 🔧 Power Query Steps & Transformations Applied

### Overview

This document outlines all Power Query transformations applied to prepare data for Power BI analysis.

---

## 📋 Global Transformations

### 1. Column Name Formatting - Remove Underscores

**Applied To**: All tables  
**Purpose**: Convert snake_case column names to proper Title Case for readability

**Examples**:

- `customer_id` → `Customer ID`
- `order_status` → `Order Status`
- `total_payment_value` → `Total Payment Value`
- `avg_review_score` → `Avg Review Score`

---

### 2. Column Capitalization - Standardize Case

**Applied To**: All text columns  
**Purpose**: Ensure consistent capitalization (Title Case for proper nouns, lowercase for descriptions)

**Examples**:

- `SAO PAULO` → `São Paulo`
- `rio de janeiro` → `Rio de Janeiro`
- `FURNITURE_DECOR` → `Furniture Decor`

---
