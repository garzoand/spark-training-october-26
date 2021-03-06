import pyspark
from pyspark.sql import SparkSession

def create_spark_env(appName, local=False):
    conf = pyspark.SparkConf()
    # conf.get(..)
    # conf.set(..)
    conf.setAppName(appName)
    if local:
        conf.setMaster('local')
    sc = pyspark.SparkContext(conf=conf)
    spark = SparkSession(sc)
    return (sc, spark)


# 1. Yarn (what we'll do)
# 2. Kubernetes (beta)
# 3. Standalone (Mesos)
