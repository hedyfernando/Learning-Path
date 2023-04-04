import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch

def queryPostgresql():
    conn_string= "dbname='company' host='localhost' user='postgres' password='cicak'"
    conn=db.connect(conn_string)
    df=pd.read_sql("select partner,total_charges from telco_users where total_charges <> 0", conn)
    df.to_csv('/home/cicak/folder_data/folder_tujuan_dag/postgresdata.csv')
    print("------Berhasil Disimpan-------")


def insertElasticsearch():
    es = Elasticsearch("http://localhost:9200") 
    df=pd.read_csv('/home/cicak/folder_data/folder_tujuan_dag/postgresdata.csv')
    for i, r in df.iterrows():
        doc=r.to_json()
        res=es.index(index="partnertotalpostgres",body=doc)
        print(res)


default_args = {
    'owner': 'hedy',
    'start_date': dt.datetime(2022, 10, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('Postgres_to_ES_DAG',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),
         ) as dag:
    
    getData = PythonOperator(task_id='GetDatabyQuery',
                             python_callable=queryPostgresql)
    
    insertData = PythonOperator(task_id='InserDatatoES',
                                python_callable=insertElasticsearch)
    

getData >> insertData