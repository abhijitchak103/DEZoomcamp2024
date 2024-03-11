# Workshop 2 - RisingWave

## Data Streaming with RisingWave

### Question 1 

Create a materialized view to compute the average, min and max trip time between each taxi zone.
From this MV, find the pair of taxi zones with the highest average trip time. You may need to use the dynamic filter pattern for this.
Bonus (no marks): Create an MV which can identify anomalies in the data. For example, if the average trip time between two zones is 1 minute, but the max trip time is 10 minutes and 20 minutes respectively.

- Yorkville East, Steinway
- Murray Hill, Midwood
- East Flatbush/Farragut, East Harlem North
- Midtown Center, University Heights/Morris Heights

```
-- CREATE_MATERIALIZED_VIEW

CREATE MATERIALIZED VIEW mat_trip_zone AS
    SELECT 
        AVG(tpep_dropoff_datetime - tpep_pickup_datetime) AS avg_trip_time,
        MIN(tpep_dropoff_datetime - tpep_pickup_datetime) AS min_trip_time,
        MAX(tpep_dropoff_datetime - tpep_pickup_datetime) AS max_trip_time,
        pulocationid,
        dolocationid
    FROM trip_data
    WHERE tpep_dropoff_datetime > tpep_pickup_datetime
    GROUP BY pulocationid, dolocationid;

WITH t AS (
    SELECT
        MAX(avg_trip_time) AS max_avg,
        pulocationid,
        dolocationid 
    FROM mat_trip_zone
    GROUP BY pulocationid, dolocationid
    ORDER BY max_avg DESC
    LIMIT 1
)
SELECT pu_zone.zone AS pickup_zone, do_zone.zone AS dropoff_zone
FROM t
JOIN taxi_zone AS pu_zone
    ON t.pulocationid = pu_zone.location_id
JOIN taxi_zone AS do_zone
    ON t.dolocationid = do_zone.location_id;
```
**Solution: Yorkville East, Steinway**

### Question 2

Recreate the MV(s) in question 1, to also find the number of trips for the pair of taxi zones with the highest average trip time.

- 5
- 3
- 10
- 1

```
-- CREATE_MATERIALIZED_VIEW

CREATE MATERIALIZED VIEW mat_trip_zone AS
    SELECT 
        COUNT(*) AS num_trips,
        AVG(tpep_dropoff_datetime - tpep_pickup_datetime) AS avg_trip_time,
        MIN(tpep_dropoff_datetime - tpep_pickup_datetime) AS min_trip_time,
        MAX(tpep_dropoff_datetime - tpep_pickup_datetime) AS max_trip_time,
        pulocationid,
        dolocationid
    FROM trip_data
    WHERE tpep_dropoff_datetime > tpep_pickup_datetime
    GROUP BY pulocationid, dolocationid;

WITH t AS (
    SELECT MAX(avg_trip_time) AS max_avg, pulocationid, dolocationid 
    FROM mat_trip_zone
    GROUP BY pulocationid, dolocationid
    ORDER BY max_avg DESC
    LIMIT 1
)
SELECT atz.num_trips
FROM t
JOIN mat_trip_zone AS atz
    ON t.pulocationid = atz.pulocationid AND t.dolocationid = atz.dolocationid;
```

**Solution: 1**

### Question 3

From the latest pickup time to 17 hours before, what are the top 3 busiest zones in terms of number of pickups? For example if the latest pickup time is 2020-01-01 12:00:00, 
then the query should return the top 3 busiest zones from 2020-01-01 11:00:00 to 2020-01-01 12:00:00.

HINT: You can use dynamic filter pattern to create a filter condition based on the latest pickup time.

NOTE: For this question 17 hours was picked to ensure we have enough data to work with.

- Clinton East, Upper East Side North, Penn Station
- LaGuardia Airport, Lincoln Square East, JFK Airport
- Midtown Center, Upper East Side South, Upper East Side North
- LaGuardia Airport, Midtown Center, Upper East Side North

```
-- CREATE_MATERIALIZED_VIEW
CREATE MATERIALIZED VIEW latest_pickup AS
    SELECT MAX(tpep_pickup_datetime) AS pickup_datetime
    FROM trip_data;

WITH t AS (
    SELECT
        COUNT(*) AS num_trips,
        trip_data.pulocationid
    FROM latest_pickup, trip_data
    WHERE trip_data.tpep_pickup_datetime > (latest_pickup.pickup_datetime - interval '17 hours')
    GROUP BY trip_data.pulocationid
    ORDER BY 1 DESC
    LIMIT 3
)
SELECT taxi_zone.zone
FROM t
JOIN taxi_zone AS taxi_zone
    ON t.pulocationid = taxi_zone.location_id;
```

**Solution: LaGuardia Airport, Lincoln Square East, JFK Airport**
