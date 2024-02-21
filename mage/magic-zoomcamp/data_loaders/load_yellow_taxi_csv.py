import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url_base = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_'
    month = '2019-01'
    extension = '.csv.gz'

    url = url_base + month + extension

    months = ['2019-02', '2019-03', '2019-04', '2019-05', '2019-06', 
            '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', 
            '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', 
            '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',]

    taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'RatecodeID': pd.Int64Dtype(),
        'store_and_fwd_flag': str,
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'payment_type': pd.Int64Dtype(),
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'improvement_surcharge': float,
        'total_amount': float,
        'congestion_surcharge': float 
    }

    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    df = pd.read_csv(url, sep=',', compression='gzip', parse_dates=parse_dates)

    for month in months:
        url = url_base + month + extension
        print(f'Reading from: {url}')
        df_current = pd.read_csv(url, sep=',', compression='gzip', parse_dates=parse_dates)
        df = pd.concat([df, df_current], ignore_index=True)
        print(f'Number of rows after appending {month}: {df.shape[0]}')
        print('-'*50)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'