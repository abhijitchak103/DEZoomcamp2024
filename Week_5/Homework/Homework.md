# Week 5 Homework

## Working with Spark

### Q1. What is the spark version? 

**Solution: 3.4.2**

### Q2. What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)?

- 1MB
- 6MB
- 25MB
- 87MB

```
total 39M
-rw-r--r-- 1 <user> <user>    0 Mar  2 12:37 _SUCCESS
-rw-r--r-- 1 <user> <user> 6.4M Mar  2 12:37 part-00000-5b14061e-581a-4f33-b0d0-f40dcd8fcec0-c000.snappy.parquet
-rw-r--r-- 1 <user> <user> 6.4M Mar  2 12:37 part-00001-5b14061e-581a-4f33-b0d0-f40dcd8fcec0-c000.snappy.parquet
-rw-r--r-- 1 <user> <user> 6.4M Mar  2 12:37 part-00002-5b14061e-581a-4f33-b0d0-f40dcd8fcec0-c000.snappy.parquet
-rw-r--r-- 1 <user> <user> 6.4M Mar  2 12:37 part-00003-5b14061e-581a-4f33-b0d0-f40dcd8fcec0-c000.snappy.parquet
-rw-r--r-- 1 <user> <user> 6.4M Mar  2 12:37 part-00004-5b14061e-581a-4f33-b0d0-f40dcd8fcec0-c000.snappy.parquet
-rw-r--r-- 1 <user> <user> 6.4M Mar  2 12:37 part-00005-5b14061e-581a-4f33-b0d0-f40dcd8fcec0-c000.snappy.parquet

```

**Solution: 6MB**

### Q3. How many taxi trips were there on the 15th of October?

- 108,164
- 12,856
- 452,470
- 62,610

```
spark.sql(
"""
SELECT 
    COUNT(1) AS October_15_trips    
FROM
    trips
WHERE 
    CAST(pickup_datetime AS DATE) = "2019-10-15"
"""
).show()
```
```
+----------------+
|October_15_trips|
+----------------+
|           62610|
+----------------+
```

**Solution: 62,610**

### Q4. What is the length of the longest trip in the dataset in hours?

- 631,152.50 Hours
- 243.44 Hours
- 7.68 Hours
- 3.32 Hours

```
spark.sql("""
SELECT 
    MAX(DATEDIFF(hour, pickup_datetime, dropOff_datetime)) as max_trip_duration_hours
FROM 
    trips
""").show()
```
```
+-----------------------+
|max_trip_duration_hours|
+-----------------------+
|                 631152|
+-----------------------+
```

**Solution: 631,152.50 Hours**

### Q5. Spark’s User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080

**Solution: 4040**

### Q6. Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?

- East Chelsea
- Jamaica Bay
- Union Sq
- Crown Heights North

```
spark.sql("""
SELECT 
    z.Zone, 
    COUNT(1) as trips_count
FROM 
    trips as t
JOIN 
    zones as z
ON 
    t.PUlocationID = z.LocationID
GROUP BY 
    z.Zone
ORDER BY 
    trips_count ASC
LIMIT 1
""").show()
```
```
+-----------+-----------+
|       Zone|trips_count|
+-----------+-----------+
|Jamaica Bay|          1|
+-----------+-----------+
```

**Solution: Jamaica Bay**