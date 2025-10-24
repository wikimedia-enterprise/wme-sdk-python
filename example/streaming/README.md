# Realtime Streaming API
This API is used to get a stream of server-sent events (SSE) related to new article create, article update, article visibility-change, article move and article delete, from all the supported projects and namespaces. The events follow [this](https://gitlab.wikimedia.org/repos/wme/wikimedia-enterprise/-/blob/main/general/schema/article.go) schema.
Allows for filtering and field selection.
Allows for parallel connection to the API.
Allows to reconnect to the API and start consuming from a certain offset/timestamp.
At the moment, the retention period (for the events) in the realtime streaming API is 48 hours.
The connection is long-lived. One does not have to reconnect due to the fact that `access token` that was used for connection has expired after 24 hours.

Refer to the documentation [here](https://enterprise.wikimedia.com/docs/realtime/).

## Running the Application

To run the application, use the following command from the project's root:

```sh
python -m example.streaming.streaming
```

## Stopping the Application

To stop the application, use the following on the terminal:

```sh
ctrl + c
```

## Examples

Connect to realtime streaming using filters and field selection.

```bash
POST https://realtime.enterprise.wikimedia.com/v2/articles
```

with request parameters:
```json
{
  "fields": [
    "name",
    "is_part_of.*",
    "event.*"
  ],
  "filters": [
    {
      "field": "namespace.identifier",
      "value": 0
    }
  ]
}
```

Response:

```bash
.
.
{"name":"El franctirador de Donbass","is_part_of":{"identifier":"cawiki","url":"https://ca.wikipedia.org","size":{}},"event":{"identifier":"efb5d726-241f-45ae-a2b8-c66fdf871286","type":"update","date_created":"2023-08-01T20:10:56.083689Z","date_published":"2023-08-01T20:10:56.084Z","partition":5,"offset":3611387}}

 {"name":"Polygonum aschersonianum","is_part_of":{"identifier":"svwiki","url":"https://sv.wikipedia.org","size":{}},"event":{"identifier":"8f0f388e-cda8-4032-b696-3b702673ab1e","type":"update","date_created":"2023-08-01T19:30:29.529004Z","date_published":"2023-08-01T19:30:29.529Z","partition":0,"offset":3614782}}


 {"name":"Haunted Mansion (2023 film)","is_part_of":{"identifier":"enwiki","url":"https://en.wikipedia.org","size":{}},"event":{"identifier":"1e598f28-2919-4b49-bba2-5a7f10de2e8f","type":"update","date_created":"2023-08-01T19:31:57.03241Z","date_published":"2023-08-01T19:31:57.033Z","partition":4,"offset":3593806}}

 {"name":"Желябовский сельский совет","is_part_of":{"identifier":"ruwiki","url":"https://ru.wikipedia.org","size":{}},"event":{"identifier":"3a52a941-0a18-4514-a93b-7fb8aff81960","type":"update","date_created":"2023-08-01T19:36:35.931726Z","date_published":"2023-08-01T19:36:35.932Z","partition":8,"offset":3588693}}
 {"name":"Iredalea","is_part_of":{"identifier":"nlwiki","url":"https://nl.wikipedia.org","size":{}},"event":{"identifier":"82775ac1-fd4d-4d4d-a6bf-2a94bab198c8","type":"update","date_created":"2023-08-01T19:36:36.007086Z","date_published":"2023-08-01T19:36:36.007Z","partition":8,"offset":3588694}}


{"name":"Писарівка_(Ямпільський_район)","is_part_of":{"identifier":"ukwiki","url":"https://uk.wikipedia.org","size":{}},"event":{"identifier":"e7c1b0c2-94b8-430e-80d2-fde6d9c40aa9","type":"delete","date_created":"2023-08-01T19:41:29.803635Z","date_published":"2023-08-01T19:41:29.98Z","partition":7,"offset":3643817}}
.
.

```

## Parallel connection
Here are the query parameters that the API supports:

```
since (string)               e.g., Since date in RFC3339 (‘2006-01-02T15:04:05Z’)
fields (array)               e.g., ["name", "is_part_of.*"]
filters (array)              e.g., [ {"field": "in_language.identifier", "value":"en"} ]
parts (array of integers)    e.g., [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
offsets (map of string:int)  e.g., {"0": 3614782, "4": 3593806, "8": 3588693}
since_per_partition (map of string:string date in RFC3339)
                             e.g., {"1": "2023-06-05T12:00:00Z",
                                    "2": "2023-06-05T12:00:00Z"}

```

All the query parameters are optional.

`parts` request parameter (array of integers) allows to target subsets of partitions in each of the parallel connections. The max allowed number of parallel connections to realtime API is 10, i.e., the allowed range for parts is 0 through 9. This means that if one were to open 10 parallel connections, they will have to target 1/10 th of partitions in each of the parallel connections to consume from all the partitions. The parts parameter passed in those 10 parallel connections will be as follows:

Considering we have 50 total partitions (0 through 49):
```
Connection  1 "parts": [0] -> this will connect to partitions  0 through  4
Connection  2 "parts": [1] -> this will connect to partitions  5 through  9
Connection  3 "parts": [2] -> this will connect to partitions 10 through 14
Connection  4 "parts": [3] -> this will connect to partitions 15 through 19
Connection  5 "parts": [4] -> this will connect to partitions 20 through 24
Connection  6 "parts": [5] -> this will connect to partitions 25 through 29
Connection  7 "parts": [6] -> this will connect to partitions 30 through 34
Connection  8 "parts": [7] -> this will connect to partitions 35 through 39
Connection  9 "parts": [8] -> this will connect to partitions 40 through 44
Connection 10 "parts": [9] -> this will connect to partitions 45 through 49
```

Using parts, one can open parallel connections in several configurations and target the partitions in different ways. The example below has two parallel connections.

Considering we have 50 total partitions (0 through 49):
```
Connection 1 "parts": [0, 1, 2, 3, 4] -> this will connect to partitions  0 through 24
Connection 2 "parts": [5, 6, 7, 8, 9] -> this will connect to partitions 25 through 49
```

One may simply have one connection with all the partitions targeted as follows:

Considering we have 50 total partitions (0 through 49):
```
Connection 1 "parts": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] -> this will connect to partitions 0 through 49
```

Please note that if using parts, one must take care to include all the possible parts across different parallel connections. This ensures that all the events from all the partitions are being delivered to the client. For instance, if one were to open a total of two parallel connections (as follows), where they forgot to include part 5, events from partitions 25 through 29 will not be delivered to the client.

Considering we have 50 total partitions (0 through 49):
```
Connection 1 "parts": [0, 1, 2, 3, 4] -> this will connect to partitions  0 through 24
Connection 2 "parts": [6, 7, 8, 9]    -> this will connect to partitions 30 through 49
```


## Reconnecting to the realtime streaming
Note that `event` is included in each article emitted by the API as shown in the example above.
The following values are useful for reconnection.

```
partition (int): the partition this event belongs to. At the moment, there are 50 total partitions.

offset (int): this event’s offset in the partition it belongs to.

date_published (string date in RFC3339): timestamp when this event was published to the partition it belongs to.
```

While consuming the articles, we record for each partition either:
```
partition -> latest offset consumed
partition -> latest date_published consumed
```

We make use of the above record to reconnect in one of the following ways:

a) Using `offsets` per partition
One can pass a map of partition:offset, e.g., {"0": 3614782, "4": 3593806, "8": 3588693}. With this example offsets, the client will receive events with offset >= 3614782 from partition 0.

If the offsets contain irrelevant partitions, they will simply be ignored. For example, for the following query parameters, partition 5 will be ignored since the relevant partitions here are 0 through 4.

```json
params = {
     "parts": [0],
     "offsets": {"0": 3614782, "4": 3593806, "5": 3588693}
}
```

For the relevant partitions (1, 2, 3) not included in the offsets in the above params, the client will receive events as they appear from those partitions (latest first).

The length/size of the offsets must be <= 50 (capped by the total number of partitions).


b) Using `since`
If we have the record for `partittion -> date_published` as follows:

```
0 -> "2024-02-29T19:41:29.98Z"
1 -> "2024-02-29T118:41:29.98Z"
2 -> "2024-02-29T18:41:26.98Z"
3 -> "2024-02-29T18:41:27.98Z"
.
.

```

Consider that the `date_published` for partition 2 is the minimum. Then, we can reconnect using minimum date_published as `since` as follows. Note that we may receive some events that we have received already before (from other partitions such as 0, 1, 3,...). This needs to be handled on the client end.

```json
params = {
       "since": "2024-02-29T18:41:26.98Z"
}
```

c) Using `since_per_partition`
This way of reconnection is not recommended due to performance issues. Please use a) or b) instead.

As a query parameter, one can pass a map of `int:string date in RFC3339`. e.g, {"1": "2023-06-05T12:00:00Z", "2": "2023-06-05T12:00:00Z"}. With this example since_per_partition, the client will receive events with date_published >= time 2023-06-05T12:00:00Z from partition 1, and so on for other partitions.

If the since_per_partition contains irrelevant partitions, they will simply be ignored. For example, for the following query parameters, partition 5 will be ignored since the relevant partitions are 0 through 4.

```json
params = {
       "parts": [0],
       "since_per_partition": {"1": "2023-06-05T12:00:00Z", "5": "2023-06-05T12:00:00Z"}
}
```

For the relevant partitions (0, 2, 3, 4) not included in the since_per_partition in the above params, the client will receive events as they appear from those partitions (latest first).

The length/size of the since_per_partition must be <= 50 (capped by the total number of partitions).
