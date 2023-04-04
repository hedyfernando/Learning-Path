import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import pandas as pd
from elasticsearch import Elasticsearch
import psycopg2 as db

def queryPostgresql():
    conn_string= "dbname='company' host='localhost' user='postgres' password='cicak'"
    conn=db.connect(conn_string)
    df=pd.read_sql("select customer_id, monthly_charges,total_charges, case \
                   when churn='No' Then 'Loyal' else 'Not Loyal' End as jenis \
                   from telco_users order by jenis,monthly_charges desc;", conn)
    df.to_csv('/home/cicak/folder_data/folder_tujuan_dag/loyal_cust.csv')
    print("------Berhasil Disimpan-------")


def insertElasticsearch():
    es = Elasticsearch("http://localhost:9200") 
    df=pd.read_csv('/home/cicak/folder_data/folder_tujuan_dag/loyal_cust.csv')
    for i, r in df.iterrows():
        doc=r.to_json()
        res=es.index(index="loyal_customer",body=doc)
        print(res)


default_args = {
    'owner': 'hedy',
    'start_date': dt.datetime(2022, 10, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('MyLoyalES',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),
         ) as dag:
    
    getData = PythonOperator(task_id='GetDatabyQuery',
                             python_callable=queryPostgresql)
    
    insertData = PythonOperator(task_id='InserDatatoES',
                                python_callable=insertElasticsearch)
    

getData >> insertData