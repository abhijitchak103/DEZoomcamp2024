import io
import pandas as pd
# import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load data from url
    """
    url_base = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-'

    url_initial = url_base + '01.parquet'

    next_months = ['02.parquet', '03.parquet', '04.parquet', '05.parquet',
            '06.parquet', '07.parquet', '08.parquet', '09.parquet', 
            '10.parquet', '11.parquet', '12.parquet']

    print(f'Reading from: {url_initial}')
    df = pd.read_parquet(url_initial)
    print('-'*50)
    print(f'Number of rows: {df.shape[0]}')

    for month in next_months:
        url_current = url_base + month
        print(f'Reading from: {url_current}')
        df_current = pd.read_parquet(url_current)
        df = pd.concat([df, df_current], ignore_index=True)
        print('-'*50)
        print(f'Number of rows: {df.shape[0]}')

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
