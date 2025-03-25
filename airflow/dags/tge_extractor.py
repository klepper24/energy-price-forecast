from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta
from typing import List

from codes.tge_scrapper import scrape 

# Default arguments for the DAG
default_args = {
    'owner': 'Michal Klepacki',
    'depends_on_past': False,
    'email': ['m.j.klepacki@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='tge_scraper',
    default_args=default_args,
    description='A DAG for scraping data from TGE',
    schedule_interval='0 9 * * *',  # Every day at 9 AM Polish time
    start_date=days_ago(1),
    catchup=False,
    tags=['webscraping', 'tge'],
) as dag:


    @task
    def scrape_data() -> None:
        
        scrape()

    # Task dependencies
    scrape_data()