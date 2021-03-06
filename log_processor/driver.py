import pyspark
from pyspark.sql import SparkSession
import pipeline
import utils

## Constants ##
###############
ACCESS_LOG_INPUT = 'sample_data/unit-test2.log'
EVIL_IP_INPUT = 'sample_data/ip-list.txt'
LOG_DF_OUTPUT = 'output/access_logs'
ALARM_DF_OUTPUT = 'output/alarms'


## Spark Env. Creation ##
#########################
(sc, spark) = utils.create_spark_env('LogProcessor', local=True)

## Processing happens ###
########################

### "Configure" input ###
access_log_rdd = sc.textFile(ACCESS_LOG_INPUT)
evil_ip_rdd = sc.textFile(EVIL_IP_INPUT)


### Your Data processing logic comes here ###
### Processing logic begin

pipeline = pipeline.LogProcessorPipeline(sc, spark)
(log_df, stat_df, alarm_df) = pipeline.build_pipeline(access_log_rdd, evil_ip_rdd)

### Processing logic end


### "Configure" output ###
log_df.write \
    .format('parquet') \
    .mode('overwrite') \
    .partitionBy('date') \
    .save(LOG_DF_OUTPUT)

stat_df.write \
    .format('jdbc') \
    .option('url', 'jdbc:mysql://localhost/spark_test') \
    .option('dbtable', 'log_report') \
    .option('user', 'spark') \
    .option('driver', 'com.mysql.jdbc.Driver') \
    .option('password', 'spark123') \
    .option('numPartition', '1') \
    .save()

alarm_df.coalece(1).write \
    .format('json') \
    .mode('overwrite') \
    .save(ALARM_DF_OUTPUT)

#### Clean up ###
#################

sc.stop()
