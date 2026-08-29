from pyspark import pipelines as dp

@dp.table(name="izwe48catalog.we48db.we48_sdp_shipment")
def load_shipments():
    df=spark.read.table("izwe48catalog.we48db.bronze_shipments")
    df2=df.filter("role='Dispatcher'")
    return df2



# @dp.table - defult take function name as target table name 
#           - overwrite with name arg

# decorator its doining somthing like ->  df2.write.saveAsTable(name)
# since as we are reading table spark.read.table()- batch  it will create materialized view