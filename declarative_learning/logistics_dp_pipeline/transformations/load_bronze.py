from pyspark import pipelines as dp


base_path="/Volumes/catalog_we48/logistics_sdp/datalake"
@dp.table(name="catalog_we48.logistics_sdp.bronze_staff_data1")
def load_staff_data():
    df=spark.readStream.format("cloudFiles") \
        .option("cloudFiles.format", "csv") \
        .option("cloudFiles.inferColumnTypes", "true") \
        .option("cloudFiles.schemaEvolutionMode","addNewColumns")\
        .load(f"{base_path}/staff1")
    return df 
    

@dp.table(name="catalog_we48.logistics_sdp.bronze_geotag_data")
def load_geotag_data():
    df=spark.readStream.format("cloudFiles") \
        .option("cloudFiles.format", "csv") \
        .option("cloudFiles.inferColumnTypes", "true") \
        .option("cloudFiles.schemaEvolutionMode","addNewColumns")\
        .load(f"{base_path}/geotag")
    return df 


@dp.table(name="catalog_we48.logistics_sdp.bronze_shipment_data")
def load_shipment_data():
    df=(spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")   
        .option("multiline","true")
        .load(f"{base_path}/shipment").select("shipment_id", "order_id", "source_city", "destination_city",
                "shipment_status", "cargo_type", "vehicle_type", "payment_mode",
                "shipment_weight_kg", "shipment_cost", "shipment_date"))
    return df 





