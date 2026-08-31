# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # MySQL → Lakehouse Federation → Lakeflow Declarative Pipelines CDC → Medallion Architecture
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC > Snapshot-diff CDC  --> Each pipeline run re-reads the full table through the foreign catalog, and AUTO CDC FROM SNAPSHOT diffs it against the previous run to infer inserts/updates/deletes ---> Small/medium tables
# MAGIC
# MAGIC
# MAGIC > Log-based CDC (Lakeflow Connect) ----> A managed connector reads the MySQL binlog directly via a gateway, independent of foreign catalogs --->production, high-volume tables

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Run this against your MySQL instance MySQL Workbench
# MAGIC
# MAGIC `CREATE DATABASE IF NOT EXISTS salesdb;`
# MAGIC
# MAGIC `USE salesdb;`

# COMMAND ----------

# MAGIC %md
# MAGIC ### Dimension: customers (SCD Type 1 target in silver — we only care about current state)
# MAGIC
# MAGIC
# MAGIC `CREATE TABLE IF NOT EXISTS customers (
# MAGIC     customer_id   BIGINT PRIMARY KEY,
# MAGIC     first_name    VARCHAR(100),
# MAGIC     last_name     VARCHAR(100),
# MAGIC     email         VARCHAR(255),
# MAGIC     city          VARCHAR(100),
# MAGIC     country       VARCHAR(100),
# MAGIC     updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# MAGIC );`
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fact: orders (SCD Type 2 target in silver — we want status history)
# MAGIC
# MAGIC `CREATE TABLE IF NOT EXISTS orders (
# MAGIC     order_id      BIGINT PRIMARY KEY,
# MAGIC     customer_id   BIGINT,
# MAGIC     order_status  VARCHAR(20),              -- PLACED, PAID, SHIPPED, DELIVERED, CANCELLED
# MAGIC     order_amount  DECIMAL(10,2),
# MAGIC     order_ts      TIMESTAMP,
# MAGIC     updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
# MAGIC     CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
# MAGIC );`

# COMMAND ----------

# MAGIC %md
# MAGIC ### initial Load

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO customers (customer_id, first_name, last_name, email, city, country) VALUES
# MAGIC (1, 'Asha',   'Rao',     'asha.rao@example.com',     'Chennai',   'India'),
# MAGIC (2, 'Liam',   'Ng',      'liam.ng@example.com',      'Singapore', 'Singapore'),
# MAGIC (3, 'Maria',  'Silva',   'maria.silva@example.com',  'Lisbon',    'Portugal'),
# MAGIC (4, 'Omar',   'Haddad',  'omar.haddad@example.com',  'Dubai',     'UAE'),
# MAGIC (5, 'Priya',  'Menon',   NULL,                        'Bengaluru', 'India')   
# MAGIC ON DUPLICATE KEY UPDATE first_name = VALUES(first_name);

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO orders (order_id, customer_id, order_status, order_amount, order_ts) VALUES
# MAGIC (1001, 1, 'PLACED',   249.99, NOW()),
# MAGIC (1002, 2, 'PAID',     89.50,  NOW()),
# MAGIC (1003, 3, 'SHIPPED',  512.00, NOW()),
# MAGIC (1004, 4, 'DELIVERED',75.25,  NOW()),
# MAGIC (1005, 1, 'PLACED',   -10.00, NOW())      
# MAGIC ON DUPLICATE KEY UPDATE order_status = VALUES(order_status);

# COMMAND ----------

# MAGIC %md
# MAGIC After completing one pipeline run insert into mysql again and try

# COMMAND ----------

# MAGIC %md
# MAGIC ### INSERT: a brand new order
# MAGIC `
# MAGIC INSERT INTO orders (order_id, customer_id, order_status, order_amount, order_ts)
# MAGIC VALUES (1006, 2, 'PLACED', 129.00, NOW());
# MAGIC `
# MAGIC  
# MAGIC ### UPDATE: order progresses through its lifecycle
# MAGIC ### in the silver SCD2 table, this closes the PLACED row and opens a PAID row
# MAGIC `
# MAGIC UPDATE orders SET order_status = 'PAID' WHERE order_id = 1001;
# MAGIC `
# MAGIC  
# MAGIC ### UPDATE: customer moves city
# MAGIC `
# MAGIC UPDATE customers SET city = 'Coimbatore' WHERE customer_id = 1;
# MAGIC `
# MAGIC  
# MAGIC ### FIX: correct the bad seed row so you can show a previously-dropped row
# MAGIC ### start passing DQ checks on the next run
# MAGIC `
# MAGIC UPDATE customers SET email = 'priya.menon@example.com' WHERE customer_id = 5;
# MAGIC UPDATE orders SET order_amount = 45.00 WHERE order_id = 1005;
# MAGIC `
# MAGIC  
# MAGIC ### DELETE: cancel and remove an order
# MAGIC ### AUTO CDC FROM SNAPSHOT detects this automatically on the next pipeline 
# MAGIC `
# MAGIC DELETE FROM orders WHERE order_id = 1004;
# MAGIC `

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from retail.gold.customer_ltv
