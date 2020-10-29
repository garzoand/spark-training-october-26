import pyspark
import pandas as pd
import utils
import pipeline


if __name__ == '__main__':
    (sc, spark) = utils.create_spark_env('LogProcessor', local=True)

    ## Run Unit Test #1

    ## Run Unit Test #2

    # Clean up
    sc.stop()
