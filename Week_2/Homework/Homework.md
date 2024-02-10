## Homework Week 2

Orchestration Examples and solutions

### Setup the data

```
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load data from url
    """
    url_base = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/'

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

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    url_initial = url_base + 'green_tripdata_2020-10.csv.gz'

    next_urls = ['green_tripdata_2020-11.csv.gz', 'green_tripdata_2020-12.csv.gz']

    df = pd.read_csv(url_initial, sep=',', compression='gzip', parse_dates=parse_dates)

    for url in next_urls:
        url_current = url_base + url
        df_current = pd.read_csv(url_current, sep=',', compression='gzip', parse_dates=parse_dates)
        df = pd.concat([df, df_current], ignore_index=True)

    return df
```

### Question 1: Data Loadking

Once the dataset is loaded, what's the shape of the data?

**Solution: 266855 rows x 20 columns**

### Question 2: Data Transformation

Upon filtering the dataset where the passenger count is greater than 0 and the trip distance is greater than zero, how many rows are left?

```
@transformer
def transform(data, *args, **kwargs):
    """
    Remove rows with 0 passenger counts and trip distances.
    Convert column names to smallcase
    Create new column to host lpep_pickup_datetime date objects
    """
    # Passenger Counts > 0
    data = data[data['passenger_count'] > 0]

    # Trip distance > 0
    data = data[data['trip_distance'] > 0]

    # Change columns names to snake_case
    columns = {
        'VendorID': 'vendor_id',
        'RatecodeID': 'rate_code_id', 
        'PULocationID': 'pu_location_id', 
        'DOLocationID': 'do_location_id',
    }

    data = data.rename(columns=columns)

    # lpep_pickup_date column
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    return data 


@test
def test_output(output, *args) -> None:
    """
    Assertion block for vendor id.
    """
    assert 'vendor_id' in output.columns, 'vendor_id missing in column names.'


@test
def test_output(output, *args) -> None:
    """
    Assertion block for passenger count.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'Output has 0 passenger count rows.'


@test
def test_output(output, *args) -> None:
    """
    Assertion block for trip distance.
    """
    assert output['trip_distance'].isin([0]).sum() == 0, 'Output has 0 trip distance rows.'
```

**Solution: 139370 rows**

### Question 3: Data Transformation
Which of the following creates a new column lpep_pickup_date by converting lpep_pickup_datetime to a date?

**Solution: data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date**

### Question 4: Data Transformation
What are the existing values of VendorID in the dataset?

**Solution: 1 or 2.**

### Question 5: Data Transformation
How many columns need to be renamed to snake case?

**Solution: 4**

### Question 6: Data Exporting
Once exported, how many partitions (folders) are present in Google Cloud?

```
@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'mage'  # Specify the name of the schema to export data to
    table_name = 'green_taxi'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
```

**Solution: 95 folders are created**

Links to Files:

Data Loader: 
Data Transformer:
Data Exporter: 
