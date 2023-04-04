import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd
from elasticsearch import Elasticsearch

def select_columns():
    df=pd.read_csv('/home/cicak/folder_data/data_sumber/telco_data.csv')
    df=df[['customerID','Partner','tenure','MonthlyCharges','TotalCharges']]
    df.columns=[x.lower() for x in df.columns]
    df.to_csv('column_eliminate.csv')

def filterData():
    df=pd.read_csv('column_eliminate.csv')
    df2 = df[(df['tenure']> 10) & (df['monthlycharges'] > 50.00)]
    df2.set_index('customerid', drop=True, append=False, inplace=True)
    df2.to_csv('/home/cicak/folder_data/loyalbytenureandmoney.csv')

def inserttoes():
    es = Elasticsearch("http://localhost:9200") 
    df=pd.read_csv('/home/cicak/folder_data/loyalbytenureandmoney.csv')
    for i, r in df.iterrows():
        doc=r.to_json()
        res=es.index(index="loyalbytenureandmoney",body=doc)
        print(res)

default_args = {
    'owner': 'hedy',
    'start_date': dt.datetime(2022, 10, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


with DAG('CSVTransform_to_ES',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),      
         ) as dag:

    columns_decision = PythonOperator(task_id='Choosing_Columns',
                                 python_callable=select_columns)
    
    filter_decision = PythonOperator(task_id='FilterData',
                                 python_callable=filterData)
    
    insertdb = PythonOperator(task_id='Insert_to_ES',
                              python_callable=inserttoes)

    moveFile = BashOperator(task_id='move_file',
                                 bash_command='mv /home/cicak/folder_data/loyalbytenureandmoney.csv /home/cicak/folder_data/folder_tujuan_dag')



columns_decision >> filter_decision >> insertdb >> moveFile