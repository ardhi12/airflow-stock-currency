import json
import errno
import requests
import yfinance as yf
from time import time
from os import path, mkdir
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# set default arguments to schedule DAG
default_args = {    
    'owner': 'ardhi',
    'start_date': datetime(2021, 6, 30),        
    # the number of repetitions of task instances in case of failure
    'retries': 1,
    # delay task instance to retry when failure occurs
    'retry_delay': timedelta(minutes=10),
}

def rupiah_format(value):
    """
    This function is used to change format IDR
    """        
    reverse = str(value)[::-1]
    temp_reverse_value = ""

    for index, val in enumerate(reverse):
        if (index + 1) % 3 == 0 and index + 1 != len(reverse):
            temp_reverse_value = temp_reverse_value + val + "."
        else:
            temp_reverse_value = temp_reverse_value + val

    result = temp_reverse_value[::-1]
    return result

def latest_usd_idr():
    """
    This function is used to get the latest USD currency
    """
    try:        
        response = requests.get("https://v6.exchangerate-api.com/v6/ac432da0abe6dd87ea30b9df/latest/USD", timeout=5)
        response.raise_for_status()    
        return response.json()["conversion_rates"]["IDR"]        
    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    except requests.exceptions.RequestException as err:
        return err

def get_stock_detail():
    """
    This function is used to get Amazon stock detail
    """
    try:
        amzn = yf.Ticker("AMZN")
        detail = {
            "name": amzn.info["longName"],
            "symbol": amzn.info["symbol"],
            "industry": amzn.info["industry"],
            "previousClose" : amzn.info["previousClose"]
        }
        print(detail)
    except Exception as e:
        print(e)        
    return detail

def transform(ti):
    """
    This function is used to get the latest USD currency
    """
    # xcom_pull is used to get data from airflow database
    datas = ti.xcom_pull(task_ids =[
        "get_stock_detail",
        "latest_usd_idr"
    ])
    millis = round(time() * 1000)
    usd = round(datas[0]["previousClose"])                  
    idr = usd * round(datas[1])
    idr_format = rupiah_format(idr)
    convert = {
        "timestamp": millis,
        "latest_price_usd": f"${usd}",
        "latest_price_idr": f"Rp. {idr_format}"
    }    
    return convert

def export(ti):
    """
    This function is used to export the result to JSON file
    """
    get_data = ti.xcom_pull(task_ids =[
        "transform",
        "get_stock_detail"
    ])
    path_output = "output/latest_stock_price_in_IDR.json"
    file_exists = path.isfile(path_output)
    if file_exists == True:
        with open(path_output,"r+") as file:            
            datas = json.load(file)            
            # append new data 
            datas["prices"].append(get_data[0])
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(datas, file, indent=4)
    else:        
        try:
            mkdir(path.dirname(path_output))
        except OSError as exc: 
            if exc.errno != errno.EEXIST:
                raise
        with open(path_output, 'w+') as file:
            datas = {}
            datas["company"] = get_data[1]["name"]
            datas["symbol"] = get_data[1]["symbol"]
            datas["industry"] = get_data[1]["industry"]            
            datas["prices"] = [get_data[0]]
            json.dump(datas, file, indent=4)

# create DAG object
# DAG effectively running when start_date + schedule_interval
with DAG("stock_currency", default_args=default_args, schedule_interval="@daily", catchup=False) as dag:

        # Create Tasks
        get_stock_detail_task = PythonOperator(
            task_id="get_stock_detail",
            python_callable=get_stock_detail
        )
        latest_usd_idr_task = PythonOperator(
            task_id="latest_usd_idr",
            python_callable=latest_usd_idr
        )
        transform_task = PythonOperator(
            task_id="transform",
            python_callable=transform
        )
        export_task = PythonOperator(
            task_id="export",
            python_callable=export
        )
        # create the workflow
        # group tasks of the same level using a list
        [get_stock_detail_task, latest_usd_idr_task] >> transform_task >> export_task