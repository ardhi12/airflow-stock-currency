import yfinance as yf
import requests

def get_stock_detail():
    amzn = yf.Ticker("AMZN")
    detail = {
        "name": amzn.info["longName"],
        "symbol": amzn.info["symbol"],
        "industry": amzn.info["industry"],
        "previousClose" : amzn.info["previousClose"]
    }
    return detail

def latest_usd_idr():
    """
    This function is used to get the latest USD currency
    """
    try:        
        response = requests.get('https://v6.exchangerate-api.com/v6/ac432da0abe6dd87ea30b9df/latest/USD', timeout=5)
        response.raise_for_status()    
        # return response.json()['conversion_rates']['IDR']
        return 14468.0497
    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    except requests.exceptions.RequestException as err:
        return err
    
latest_usd_idr()