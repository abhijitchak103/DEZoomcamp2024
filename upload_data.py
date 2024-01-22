print('importing required libraries...')

import pandas as pd
from time import time

from sqlalchemy import create_engine

print('...successfully imported libraries')

df = pd.read_csv('green_tripdata_2019-09.csv', nrows=100)

# We notice that the `lpep_pickup_datetime` and `lpep_dropoff_datetime` are text
# They should be datetime. We need to parse them as datetime objects

df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

# Create connection with postgres to upload data

# Create an engine:
# Syntax: create_engine('sql_provider://username:password@localhost:port/db_name')

print('trying to establish connection to pgsql...')
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
print('...successfully established connection')

## Next we creata an iterotor for inserting chunks of data to postgres
print('creating iterator...')
df_iter = pd.read_csv('green_tripdata_2019-09.csv', iterator=True, chunksize=100_000)
print('...successfully created iterator')
df = next(df_iter)

df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

# Create the table and insert the first chunk of 100,000 rows

start_first = time()

print('creating table and adding the headers/columns...')
df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')
print('...successfully created table and column names')

print('adding data to table...')

df.to_sql(name='green_taxi_data', con=engine, if_exists='append')

end_first = time()

print('...inserted first chunk in ... %.3f seconds...' % (end_first-start_first))


# Insert the subsequent 100,000 row chunks...
for df in df_iter:
    start = time()
    
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    end = time()

    print('...inserted another chunk in ... %.3f seconds...' % (end-start))

print('...successfully inserted all chunks of data into yellow_taxi_data')

print('reading zones data...')
df_zones = pd.read_csv('taxi+_zone_lookup.csv')
print('...successfully read zones')

print('inserting into a new table zones...')
df_zones.to_sql(name='zones', con=engine, if_exists='replace')
print('...successfully inserted into zones.')