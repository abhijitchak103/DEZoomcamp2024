## Question 1. Knowing docker tags

--rm : Automatically remove the container when it exits

## Question 2: Understanding docker first run
docker run command for python:3.9 in interactive mode and bash entrypoint

docker run -it --entrypoint=bash python:3.9
pip list

Gives the output:
Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.42.0

Version of package wheel=0.42.0

## Preparing Postgres

docker create network pg-network

docker run -it \
 -e POSTGRES_USER="root" \
 -e POSTGRES_PASSWORD="root" \
 -e POSTGRES_DB="ny_taxi" \
 -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
 -p 5432:5432 \
 --network=pg-network \
 --name pg-database \
 postgres:13

python upload_data.py

docker run -it \
 -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
 -e PGADMIN_DEFAULT_PASSWORD="root" \
 -p 8080:80 \
 --network=pg-network \
 --name pgadmin \
 dpage/pgadmin4

## Question 3. Count records

How many taxi trips were totally made on September 18th 2019

query: 
select count(1) from green_taxi_data
where date(lpep_pickup_datetime) = '2019-09-18'
and date(lpep_dropoff_datetime) = '2019-09-18';

Solution: 15612

## Question 4. Largest trip for each day
Which was the pick up day with the largest trip distance Use the pick up time for your calculations.

select date(lpep_pickup_datetime), trip_distance 
from green_taxi_data
order by trip_distance desc
limit 1;

Solution: 2019-09-26

## Question 5. Three biggest pick up Boroughs
Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

select 
	sum(total_amount),
	z."Borough"
from 
	green_taxi_data g 
	join
	zones z
	on g."PULocationID" = z."LocationID"
where 
	date(lpep_pickup_datetime) = '2019-09-18'
	and z."Borough" <> 'Unknown'
group by 
	z."Borough"
order by 
	sum(total_amount) desc;

Solution: Brooklyn 96333, Manhattan 92271 and Queens 78671

## Question 6. Largest tip
For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

select 
	date(lpep_pickup_datetime),
	t.tip_amount,
	zpu."Zone",
	zdo."Zone"
from
	green_taxi_data t 
	join zones zpu on 
	t."PULocationID" = zpu."LocationID"
	join zones zdo on
	t."DOLocationID" = zdo."LocationID"
where
	date_part('month', lpep_pickup_datetime) = 9 and
	date_part('year', lpep_pickup_datetime) = 2019
	and zpu."Zone" = 'Astoria'
order by
	t.tip_amount desc
limit 1;

Solution: JFK Airport