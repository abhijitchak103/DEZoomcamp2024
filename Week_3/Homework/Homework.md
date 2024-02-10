# DE Zoomcamp 2024

### Reading Data and Uploading to GCP

```python
## Load Data

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

## Export Data


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Export to GCP Bucket
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage-abhijit-1'
    object_key = 'ny_taxi_data.parquet'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )

```

### Question 1 

What is count of records for the 2022 Green Taxi Data?

**Solution: 840402**

### Question 2

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- 0 MB for the External Table and 6.41MB for the Materialized Table
- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table
- 2.14 MB for the External Table and 0MB for the Materialized Table

**Solution:**

### Question 3

How many records have a fare_amount of 0?

- 12,488
- 128,219
- 112
- 1,622

**Solution:**

### Question 4

What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

- Cluster on lpep_pickup_datetime Partition by PUlocationID
- Partition by lpep_pickup_datetime Cluster on PUlocationID
- Partition by lpep_pickup_datetime and Partition by PUlocationID
- Cluster on by lpep_pickup_datetime and Cluster on PUlocationID

**Solution:**

### Question 5

Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

Choose the answer which most closely matches.

- 22.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table
- 5.63 MB for non-partitioned table and 0 MB for the partitioned table
- 10.31 MB for non-partitioned table and 10.31 MB for the partitioned table

**Solution:**

### Question 5

Where is the data stored in the External Table you created?

- Big Query
- GCP Bucket
- Big Table
- Container Registry

**Solution:**

### Question 7

It is best practice in Big Query to always cluster your data:

- True
- False

**Solution:**

(Bonus: Not worth points) 
### Question 8

Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?