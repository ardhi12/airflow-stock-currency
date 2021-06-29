import yfinance as yf
import requests
from time import time

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

