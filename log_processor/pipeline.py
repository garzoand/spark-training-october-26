import time
import datetime
from pyspark.sql.types import *


class LogProcessorPipeline:

    def __init__(self, sc, spark):
        self.sc = sc
        self.spark = spark

    def build_pipeline(self, access_log_rdd, evil_ip_rdd):
        log_df = None
        stat_df = None
        alarm_df = None
        return (log_df, stat_df, alarm_df)
    