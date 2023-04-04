# ETL processing from SQL to NOSQL with Airflow

## Description

This project I created an ETL process, where the data pipeline that I created is:

PostgreSQL >> Airflow >> ElasticSearch

1. The CSV file is imported into PostgreSQL using python
2. Transform data from either a CSV file or PostgreSQL and send it to ElasticSearch using Python and Airflow with a predetermined schedule.
3. Visualize and create a Dashboard using Kibana

## Objective

1. Create DAG for processing data
2. Create DAG to save processed data to elasticsearch
3. Create Visualisasi with Kibana

### Technology

* Python
* Airflow (DAG)
* PostgreSQL
* ElasticSearch
* Kibana

## Authors

1. Hedy Fernando
