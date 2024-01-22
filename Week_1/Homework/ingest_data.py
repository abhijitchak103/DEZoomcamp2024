print('importing required libraries...')

import os
import pandas as pd
from time import time

import argparse

from sqlalchemy import create_engine

print('...successfully imported libraries')


def main(params):
    # Assign parameters
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_gz = 'output.csv.gz'
    csv_name = 'output.csv'

    # Download the csv
    print("downloading data...")
    os.system(f"wget {url} -O {csv_gz}")
    os.system(f"gzip -d {csv_gz}")
    print("...successfully downloaded data")

    # Create connection with postgres to upload data

    # Create an engine:
    # Syntax: create_engine('sql_provider://username:password@localhost:port/db_name')

    print('trying to establish connection to pgsql...')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print('...successfully established connection')

    ## Next we creata an iterator for inserting chunks of data to postgres
    print('creating iterator...')
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100_000)
    print('...successfully created iterator')
    df = next(df_iter)

    # We notice that the `lpep_pickup_datetime` and `lpep_dropoff_datetime` are text
    # They should be datetime. We need to parse them as datetime objects
    
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # Create the table and insert the first chunk of 100,000 rows

    start_first = time()

    print('creating table and adding the headers/columns...')
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    print('...successfully created table and column names')

    print('adding data to table...')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    end_first = time()

    print('...inserted first chunk in ... %.3f seconds...' % (end_first-start_first))


    # Insert the subsequent 100,000 row chunks...
    for df in df_iter:
        start = time()
        
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        end = time()

        print('...inserted another chunk in ... %.3f seconds...' % (end-start))

    print('...successfully inserted all chunks of data')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    
    main(args)