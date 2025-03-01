import os
import yfinance as yf

ticker="ITC.NS"
period="5y"

def fetch_data(ticker=ticker, period=period):
    """Fetch historical data and save it to a CSV file."""

    if not os.path.exists("data"):
        os.makedirs("data")

    df = yf.Ticker(ticker).history(period=period)

    csv_path = f"data/{ticker}.csv"
    df.to_csv(csv_path)

    return df
    
