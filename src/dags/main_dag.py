from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from elastic.tasks import (
    delete_indices_in_elastic_search, create_indices_in_elasticsearch,
    create_documents_in_indices, search_same_products
)
from crawls.tasks import (
    run_scraper_task_saturn, run_scraper_task_stroyudacha, 
    add_vimos_products_in_db,
)
from reports.tasks import send_reports


dag = DAG(
    'parsing_and_analize_data',
    schedule_interval=timedelta(days=1), 
    start_date=days_ago(1)
)

t1 = PythonOperator(
    task_id='crawling_saturn_data', 
    python_callable=run_scraper_task_saturn,
    dag=dag
)
t2 = PythonOperator(
    task_id='crawling_stroyudacha_data', 
    python_callable=run_scraper_task_stroyudacha,
    dag=dag
)
t3 = PythonOperator(
    task_id='vimos_data_adding', 
    python_callable=add_vimos_products_in_db,
    dag=dag
)
t4 = PythonOperator(
    task_id='delete_indices', 
    python_callable=delete_indices_in_elastic_search,
    dag=dag
)
t5 = PythonOperator(
    task_id='create_indices', 
    python_callable=create_indices_in_elasticsearch,
    dag=dag
)
t6 = PythonOperator(
    task_id='create_documents_in_indices', 
    python_callable=create_documents_in_indices,
    dag=dag
)
t7 = PythonOperator(
    task_id='create_analytic_tables', 
    python_callable=search_same_products,
    dag=dag
)
# TODO: Change to EmailOperator
t8 = PythonOperator(
    task_id='send_reports', 
    python_callable=send_reports,
    dag=dag
)

[t1, t2, t3] >> t4
t4 >> t5 >> t6 >> t7 >> t8