from pyspark.sql import HiveContext
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

hiveCtx = HiveContext(sc)

tweets = hiveCtx.read.json("/code/src/tweets.json")
tweets.registerTempTable("tweets")
results =hiveCtx.sql("SELECT user.name, text from tweets")

print(results)