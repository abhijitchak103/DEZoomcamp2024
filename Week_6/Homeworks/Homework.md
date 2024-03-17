# Week 6 Homework

## Working with Data Streaming

### Question 1: Redpanda version

```
rpk version
v23.2.26 (rev 328d83a06e)
```

### Question 2: Creating a topic

```
$ rpk topic create test-topic
TOPIC       STATUS
test-topic  OK
```

### Question 3: Connecting to the Kafka server

```
import json
import time 

from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()
```

```
True
```

### Question 4: Sending data to the stream
```
t0 = time.time()

topic_name = 'test-topic'

for i in range(10):
    message = {'number': i}
    producer.send(topic_name, value=message)
    print(f"Sent: {message}")
    time.sleep(0.05)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')
```

```
Sent: {'number': 0}
Sent: {'number': 1}
Sent: {'number': 2}
Sent: {'number': 3}
Sent: {'number': 4}
Sent: {'number': 5}
Sent: {'number': 6}
Sent: {'number': 7}
Sent: {'number': 8}
Sent: {'number': 9}
took 0.51 seconds
```

### Question 5: Sending the Trip Data
```
rpk topic create green-trips --partitions 4 --replicas 1
topic_name = 'green-trips'
t0 = time.time()
for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}

    # Send the data to the Kafka topic
    producer.send(topic=topic_name, value=row_dict)
t2 = time.time()
print(f'took {(t2 - t0):.2f} seconds')
producer.flush()
```
took 24.78 seconds

### Question 6: Parsing the data

```
root
 |-- lpep_pickup_datetime: string (nullable = true)
 |-- lpep_dropoff_datetime: string (nullable = true)
 |-- PULocationID: integer (nullable = true)
 |-- DOLocationID: integer (nullable = true)
 |-- passenger_count: double (nullable = true)
 |-- trip_distance: double (nullable = true)
 |-- tip_amount: double (nullable = true)
```

### Question 7: Most popular destination

```
DOLocationID = 74
```
