[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/david-ohayon-907b85138/)
# Voucher Selection API
## Motivation
This project attempts to show the interplay between different frameworks in the field of data. The tools that are used in this project are:
* [Apache Airflow](https://airflow.apache.org/) - Job orchestrator that executes workflows
* [Docker](https://www.docker.com/) - containerisation and standardisation of processes
* [Postgres](https://www.postgresql.org/) - Database to store data

This project uses Python, SQL and BASH. On top of that, Dockerfiles, docker-compose files, XMLs and some HTML were also 
written.

## Problem
The problem that is dealt with in this project is the analysis of a dataset which includes cleaning and transforming it,
in order to derive what is the most used voucher value among predefined customer segments.
The segments are as follows:

|   Segment      | Segment Name | Measure |
| ------------ | ------------------------- | ------------------------ |
| Frequent    | "1-4"                | total orders                |
| Frequent    | "5-13"                | total orders               |
| Frequent    | "14-37"              | total orders                |
| Recency     | "30-60"              | days since last order       |
| Recency     | "61-90"              | days since last order       |
| Recency     | "91-120"             | days since last order       |
| Recency     | "121-180"            | days since last order       |
| Recency     | "180+"               | days since last order       |

Due to the fact that the dataset handles entries from 2018, this project assumes to be in a different point in time (2018-09-15).
This value can be adjusted by changing the `CUR_DATE` environment variable in the docker-compose file (for both Airflow and the API).

The choice behind using a different timeline is to allow for having results that are more varied in comparison to having all
customers fall into one category (i.e. recency 180+ days). 

### Data Cleaning
The dataset was filtered and cleaned according to the following criteria:
* Only entries holding the `Peru` country code were included
* Entries with `total_orders` of 0 but with `last_order_ts` or `first_order_ts` were discarded.
* Entries with `last_order_ts` that took place before `first_order_ts` were discarded.
* Entries with null `total_orders` or `voucher_amount` were discarded.

Note: entries in the frequent segment were counted in a custom segment `out_of_range`. This
can be seen in the code and also viewed in the `selection_criteria` API endpoint. 
 
## Requirements
In order to run this project, Docker needs to be installed and running (on MacOS, ensure sufficient resources are
dedicated via Docker preferences). Furthermore,
ensure that the ports used in the docker-compose are not blocked by other processes you might
already have running. For example if you have postgres installed and it keeps port 5432 blocked, do close the service.
##Quickstart
 
The repository's root directory contains an executable `quickstart`.
The quickstart executable can be used with 3 different options:
* `run` - runs docker-compose which spawns all relevant containers. This will print all logs to the current terminal 
window.
* `run -d` - similar to the previous command, however in detached mode where everything runs in the background.
* `stop` - tears down the environment

While being in the root directory execute the following to initialise the project:
```
./quickstart run
```

### Project Composition
This entire project is containerised and runs via Docker. Two custom built images (hosted on Dockerhu) are used
for the API container and the Airflow container (respectively found in `airflow_cfg` and in the `api_endpoint` directory). 
The postgres databases use the official image.

The docker-compose file is the entire deployment and it spawns 4 containers in total: Airflow, Postgres (twice, one for
metadb and one for data warehousing) and containerised REST API application.


Airflow is used to execute the pipeline which downloads the relevant data (extraction),
loads it to a postgres database (part of the containerised setup) and then cleans and models it using SQL.
Additional models are created that are pertinent to the problem at hand.

The database consists of 3 schemas: `raw` (raw untouched data import), `model_staging` (intermediary step) and 
`model_production` (acts as the last step where the data is served, in this case to the API).

A REST API is connected to the database and provides access to information via the following endpoints:
* `localhost:5000/selection_criteria` - displays the segmentation
* `localhost:5000/voucher` - endpoint that accepts requests (curl/ Python requests) and returns a JSON object
* `localhost:5000/search_voucher` - interface to send post requests to the API

In order to populate the database with the output, run the `voucher_selection` pipeline via Airflow (accessible on `localhost:8080`)
before interacting with the API.

### Sending a Request to the API
`Note: the request takes specific formats and these would be described in the code sample`

In order to send a request to the API outside of using the interface endpoint (`localhost:5000/search_voucher`), it is 
possible to use the Python requests package:

```
import requests

url = 'http://localhost:5000/voucher'
myobj = {
    "customer_id": 123, 
    "total_orders": 10, 
    "country_code": "Peru",
    "last_order_ts": "2018-07-18 00:00:00", # %Y-%m-%d %H:%M:%S format
    "first_order_ts": "2017-05-03 00:00:00",
    "segment_name": "frequent_segment" # takes frequent_segment or recency_segment
}

x = requests.post(url, json=myobj)

print(x.text)
```

Or an alternative would be to send a curl request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"customer_id": 123,"country_code": "Peru","last_order_ts": "2018-05-03 00:00:00", "first_order_ts": "2017-05-03 00:00:00", "total_orders": 15, "segment_name": "recency_segment"}' \
  http://localhost:5000/voucher
```


 

## Testing
This project uses the pytest framework for unittesting. 
The `tests` directory contains the relevant scripts and this should be ran from inside the Airflow container.
In order to do so you would need to exec into the container:
```
docker exec -it airflow bash

# run the tests from /opt
pytest -v -s
``` 

## Remarks
It is important to note that all credentials chosen and used in the scope of this project are meant
to be simple on purpose and security measures were not taken into consideration or use of external
secret services (such as Hashicorp Vault, which could be integrated with Airflow). The same applies
for security, permissions and appropriate data warehousing model which were not part of the scope of 
this project.

In real world scenario, there could be tools better used for SQL execution and orchestration 
(such as [DBT](https://www.getdbt.com/)). Furthermore, due to the scale of this project, extensive SQL running functions
weren't specifically written and PostgresOperators were used instead.

## Conclusion
Analysing the dataset revealed that the voucher value that repeats itself the most
among customers in Peru is the lowest tier voucher amount (2640). After segmenting the customers
the same was result was also encountered across all segments (recency and frequent).  
