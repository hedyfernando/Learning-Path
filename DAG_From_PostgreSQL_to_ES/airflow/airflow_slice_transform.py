import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd
from elasticsearch import Elasticsearch

def slicerange():
    df=pd.read_csv('/home/cicak/folder_data/data_sumber/telco_data.csv')
    df.drop(columns=['customerID'], inplace=True)
    df.columns=[x.lower() for x in df.columns]
    df['tenure_range'] = pd.cut(df['tenure'], [1,10,20,30,40,50,72])
    df.to_csv('/home/cicak/folder_data/tenureslice.csv')


def insertElasticsearch():
    es = Elasticsearch("http://localhost:9200") 
    df=pd.read_csv('/home/cicak/folder_data/tenureslice.csv')
    for i, r in df.iterrows():
        doc=r.to_json()
        res=es.index(index="tenureslice",body=doc)
        print(res)


default_args = {
    'owner': 'hedy',
    'start_date': dt.datetime(2022, 10, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


with DAG('Slice_Tenure',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),      # '0 * * * *',
         ) as dag:

    slicedata = PythonOperator(task_id='slice_tenure',
                                 python_callable=slicerange)
    
    insertoes = PythonOperator(task_id='insert_to_ES',
                                 python_callable=insertElasticsearch)

    moveFile = BashOperator(task_id='move',
                                 bash_command='mv /home/cicak/folder_data/tenureslice.csv /home/cicak/folder_data/folder_tujuan_dag')



slicedata >> insertoes >> moveFile