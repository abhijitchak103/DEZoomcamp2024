import pandas as pd
import io


url_base = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_'
month = '2019-01'
extension = '.csv.gz'

url = url_base + month + extension

months = ['2019-02', '2019-03', '2019-04', '2019-05', '2019-06', 
        '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12']

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

parse_dates = ['pickup_datetime', 'dropOff_datetime']

df = pd.read_csv(url, sep=',', compression='gzip', parse_dates=parse_dates)

for month in months:
    url = url_base + month + extension
    print(f'Reading from: {url}')
    df_current = pd.read_csv(url, sep=',', compression='gzip', parse_dates=parse_dates)
    df = pd.concat([df, df_current], ignore_index=True)
    print(f'Number of rows after appending {month}: {df.shape[0]}')
    print('-'*50)
