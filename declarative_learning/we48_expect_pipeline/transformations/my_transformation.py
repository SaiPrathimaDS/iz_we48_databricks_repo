from pyspark import pipelines as dp
from pyspark.sql import functions as f

@dp.table(name="get_silver_staff3")
@dp.expect("shipment_check","shipment_id is not null")
#@dp.expect_or_drop("role_check","role is not null ")
#@dp.expect_or_fail("shipment_check","shipment_id is not null")
def get_silver_staff():
    df=spark.read.table("catalog_we48.logistics_db.silver_staff") 
    return df



@dp.table(name="get_silver_staff_2")
@dp.expect_all_or_drop({"role_check":"role is not null","age_check":"age is not null"})
def get_silver_staff_2():
    df=spark.read.table("catalog_we48.logistics_db.silver_staff") 
    return df



@dp.table(name="get_silver_staff_age_error")
def get_silver_staff_age_error():
    df=spark.read.table("catalog_we48.logistics_db.silver_staff").filter("age is null")
    return df