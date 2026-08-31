# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %sql
# MAGIC select * from izwe48catalog.we48db.bronze_shipments;
# MAGIC select * from catalog_we48.logistics_db.silver_staff where age is null or role is null;
# MAGIC
# MAGIC select * from get_silver_staff;
# MAGIC
# MAGIC select * from catalog_we48.logistics_db.silver_staff where shipment_id is null;
