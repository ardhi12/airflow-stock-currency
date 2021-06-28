import yfinance as yf

def get_stock_detail():
    amzn = yf.Ticker("AMZN")
    detail = {
        "name": amzn.info["longName"],
        "symbol": amzn.info["symbol"],
        "industry": amzn.info["industry"],
        "previousClose" : amzn.info["previousClose"]
    }
    return detail

get_stock_detail()