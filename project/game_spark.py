import mysql.connector
import pandas as pd
import numpy as np


import pyspark
from pyspark.sql import Row,SQLContext
from pyspark.sql import SparkSession
from pyspark.context import SparkContext, SparkConf
from pyspark.sql import Row

conf = SparkConf().setAppName("rdd").setMaster("local[1]")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = SparkSession(sc)





df = sqlContext.read.csv('game_viewer_count.csv', header = True)



game_stream_count = df.select('game_name').rdd.map(lambda x: (x[0],1))\
    .reduceByKey(lambda a,b: a+b)\
    .collect()

game_total_viewer_count = df.select('game_name','viewer_count').rdd.map(lambda x: (x[0],int(0 if x[1] is None else float(x[1]))))\
    .reduceByKey(lambda a,b: a+b)\
    .collect()

game_average_viewer_count = df.select('game_name','viewer_count').rdd.map(lambda x: (x[0],int(0 if x[1] is None else float(x[1]))))\
    .groupByKey()\
    .mapValues(lambda x: int(sum(x) / len(x)))\
    .collect()

df1 = spark.createDataFrame(game_stream_count, schema=['game_name', 'stream_count'])
df2 = spark.createDataFrame(game_total_viewer_count, schema=['game_name', 'total_viewer_count'])
df3 = spark.createDataFrame(game_average_viewer_count, schema=['game_name', 'average_viewer_count'])

rdd_join_1 = df1.join(df2, on='game_name')
rdd_join_2 = rdd_join_1.join(df3, on='game_name')
rdd_join_2.toPandas().to_csv('game.csv')


