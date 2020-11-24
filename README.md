[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/david-ohayon-907b85138/)
# Voucher Selection API
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
This value can be adjusted by changing the `INSERT` Airflow variable.  

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

## Motivation
This project attempts to show the interplay between different frameworks in the field of data. The tools that are used in this project are:
* [Apache Airflow](https://airflow.apache.org/) - Job orchestrator that executes workflows
* [Docker](https://www.docker.com/) - containerisation and standardisation of processes
* [Postgres](https://www.postgresql.org/) - Database to store data

This project uses Python, SQL and BASH. On top of that, Dockerfiles, docker-compose files, XMLs and some HTML were also 
written.


#### Requirements:
In order to run this project, Docker needs to be installed and running. Furthermore,
ensure that the ports used in the docker-compose are not blocked by other processes you might
already have running. For example if you have postgres installed and it keeps port 5432 blocked, do close the service. 

## Quickstart  
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

## Project Composition
Airflow is used to execute the pipeline which downloads the relevant data (extraction),
loads it to a postgres database (part of the containerised setup) and then cleans and models it using SQL.
Additional models are created that are pertinent to the problem at hand. 

A REST API is connected to the database and provides access to information via the following endpoints:
* `localhost:5000/selection_criteria` - displays the segmentation
* `localhost:5000/voucher` - endpoint that accepts requests (curl/ Python requests) and returns a JSON object
* `localhost:5000/search_voucher` - interface to send post requests to the API

### Sending a Request to the API


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
secret services (such as Hashicorp Vault, which could be integrated with Airflow).

In real world scenario, there could be tools better used for SQL execution and orchestration 
(such as [DBT](https://www.getdbt.com/)).
