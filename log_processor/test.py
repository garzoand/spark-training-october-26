import pyspark
import pandas as pd
import utils
import pipeline

def get_sorted_data_frame(data_frame, columns_list):
    return data_frame.sort_values(columns_list).reset_index(drop=True)

def test_access_log_df(pipeline, test_input_rdd):
    expected_output = [
        ['109.169.248.247', "12/Dec/2015:18:25:11 +0100", '2015-12-12', 18, 'GET', '/administrator/', 'HTTP/1.1', 200],
        ['109.169.248.247', "12/Dec/2015:18:25:11 +0100", '2015-12-12', 18, 'POST', '/administrator/index.php', 'HTTP/1.1', 200],
    ]

    df_actual = pipeline.build_log_df(test_input_rdd)
    df_actual.show()

    df_expected = pipeline.spark.createDataFrame(expected_output, pipeline.access_log_schema)
    df_expected.show()

    actual = get_sorted_data_frame(df_actual.toPandas(), ['ip', 'ts', 'method', 'resource', 'protocol', 'response'])
    expected = get_sorted_data_frame(df_expected.toPandas(), ['ip', 'ts', 'method', 'resource', 'protocol', 'response'])
    pd.testing.assert_frame_equal(expected, actual, check_like=True)
    print('#### Unit Test #1 passed ####')


if __name__ == '__main__':
    (sc, spark) = utils.create_spark_env('LogProcessor', local=True)
    pipeline = pipeline.LogProcessorPipeline(sc, spark)

    ## Run Unit Test #1
    test_input_rdd = sc.textFile('sample_data/unit-test.log')
    test_access_log_df(pipeline, test_input_rdd)

    ## Run Unit Test #2

    # Clean up
    sc.stop()
