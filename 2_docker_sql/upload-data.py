print('importing required libraries...')

import pandas as pd
from time import time

from sqlalchemy import create_engine

print('...successfully imported libraries')

df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)

# To get the schema of table in sql we need to find 
# the column properties and content types
# We do so, using a convenient method `pd.io.sql.get_schema(df, table_name)`

# print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))

# The output of the above statement is:

"""
CREATE TABLE "yellow_taxi_data" (
"VendorID" INTEGER,
  "tpep_pickup_datetime" TEXT,
  "tpep_dropoff_datetime" TEXT,
  "passenger_count" INTEGER,
  "trip_distance" REAL,
  "RatecodeID" INTEGER,
  "store_and_fwd_flag" TEXT,
  "PULocationID" INTEGER,
  "DOLocationID" INTEGER,
  "payment_type" INTEGER,
  "fare_amount" REAL,
  "extra" REAL,
  "mta_tax" REAL,
  "tip_amount" REAL,
  "tolls_amount" REAL,
  "improvement_surcharge" REAL,
  "total_amount" REAL,
  "congestion_surcharge" REAL
)
"""

# We notice that the `tpep_pickup_datetime` and `tpep_dropoff_datetime` are text
# They should be datetime. We need to parse them as datetime objects

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# If we check the above schema again...

# print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))

# The output now is:
"""
CREATE TABLE "yellow_taxi_data" (
"VendorID" INTEGER,
  "tpep_pickup_datetime" TIMESTAMP,
  "tpep_dropoff_datetime" TIMESTAMP,
  "passenger_count" INTEGER,
  "trip_distance" REAL,
  "RatecodeID" INTEGER,
  "store_and_fwd_flag" TEXT,
  "PULocationID" INTEGER,
  "DOLocationID" INTEGER,
  "payment_type" INTEGER,
  "fare_amount" REAL,
  "extra" REAL,
  "mta_tax" REAL,
  "tip_amount" REAL,
  "tolls_amount" REAL,
  "improvement_surcharge" REAL,
  "total_amount" REAL,
  "congestion_surcharge" REAL
)
"""

# Create connection with postgres to upload data

# Create an engine:
# Syntax: create_engine('sql_provider://username:password@localhost:port/db_name')

print('trying to establish connection to pgsql...')
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
print('...successfully established connection')
# Now to create a postgres friendly DDL

"""print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))"""

# Now we get the output in proper postgres format

"""
CREATE TABLE yellow_taxi_data (
	"VendorID" BIGINT, 
	tpep_pickup_datetime TIMESTAMP WITHOUT TIME ZONE, 
	tpep_dropoff_datetime TIMESTAMP WITHOUT TIME ZONE, 
	passenger_count BIGINT, 
	trip_distance FLOAT(53), 
	"RatecodeID" BIGINT, 
	store_and_fwd_flag TEXT, 
	"PULocationID" BIGINT, 
	"DOLocationID" BIGINT, 
	payment_type BIGINT, 
	fare_amount FLOAT(53), 
	extra FLOAT(53), 
	mta_tax FLOAT(53), 
	tip_amount FLOAT(53), 
	tolls_amount FLOAT(53), 
	improvement_surcharge FLOAT(53), 
	total_amount FLOAT(53), 
	congestion_surcharge FLOAT(53)
)
"""

## Next we creata an iterotor for inserting chunks of data to postgres
print('creating iterator...')
df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100_000)
print('...successfully created iterator')
df = next(df_iter)

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# Create the table and insert the first chunk of 100,000 rows

start_first = time()

print('creating table and adding the headers/columns...')
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
print('...successfully created table and column names')

print('adding data to table...')

df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

end_first = time()

print('...inserted first chunk in ... %.3f seconds...' % (end_first-start_first))


# Insert the subsequent 100,000 row chunks...
for df in df_iter:
    start = time()
    
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    end = time()

    print('...inserted another chunk in ... %.3f seconds...' % (end-start))

print('...successfully inserted all chunks of data')