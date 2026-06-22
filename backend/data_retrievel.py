import yfinance as yf
import pandas as pd

def create_data(ticker):

    try:

        df = yf.download(
            ticker,
            period="5y",
            auto_adjust=True
        )

        if df.empty:
            print("No data found")
            return False

        df.to_csv("Stock_price.csv")

        print("Stock_price.csv created")

        return True

    except Exception as e:

        print("DOWNLOAD ERROR:", e)

        return False