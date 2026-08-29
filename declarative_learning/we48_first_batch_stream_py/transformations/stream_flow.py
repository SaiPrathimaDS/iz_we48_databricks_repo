from pyspark import pipelines as dp

@dp.table(name="izwe48catalog.we48db.we48_sdp_stream_shipment")
def stream_shipments():
    df=spark.readStream.table("izwe48catalog.we48db.bronze_shipments")
    df2=df.filter("role='Dispatcher'")
    return df2



# @dp.table - defult take function name as target table name 
#           - overwrite with name arg
# since as we are reading table spark.readStream.table() it will create Streaming Table