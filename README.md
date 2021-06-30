# Batch Processing of Stock Price with IDR currency
## Use Case
It is difficult to get information about the price of shares in IDR, so we have to manually convert USD to IDR. 
So we will create a data pipeline using batch processing to create a history of the daily share price in IDR and USD.  
Example of a stock used here is Amazon, Inc (AMZN).

## Workflow
![alt text](https://raw.githubusercontent.com/ardhi12/airflow-stock-currency/master/assets/graph_view_workflow.png)

## Tool
* Airflow : Scheduling tasks

## Prerequisite
* Make sure you have Python 3.6 or above installed on your machine
* Make sure you have Airflow installed on your machine
* Clone this repository  
`git clone https://github.com/ardhi12/airflow-stock-currency`
* Install the prerequisite library from requirements.txt   
`pip3 install -r requirements.txt`
* Copy stock_currency.py files to your dags directory  
`cp airflow-stock-currency/stock_currency.py <path_to_dags_directory>`

## Run
* Run `airflow webserver -p 8080` to start airflow webserver
* Run `airflow scheduler` to start airflow webserver
* Open [http://localhost:8080](http://localhost:8080) in your browser
* Activate dag by clicking the toggle

## Result
![alt text](https://raw.githubusercontent.com/ardhi12/airflow-stock-currency/master/assets/graph_view_success.png)

## Notes
* Output is a json file that will be located in `output/latest_stock_price_in_IDR.json`
* The output will update automatically according to the schedule
* Share data source comes from yahoo finance, so make sure you have an stable internet connection when running the program