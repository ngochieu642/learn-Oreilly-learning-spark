from pyspark.sql import HiveContext
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

hiveCtx = HiveContext(sc)

dataframe_mysql = hiveCtx.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://192.168.1.36:33060") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "sipiot.User") \
    .option("user", "sip") \
    .option("password", "^62UaE{]a)VT3{sp") \
    .load()

dataframe_mysql.show()