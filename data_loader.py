import os
import yfinance as yf

ticker="KOTAKBANK.NS"
period="1y"

def fetch_data(ticker=ticker, period=period):
    
    # Fetching historical data and saving it to a CSV file inside the data folder
    if not os.path.exists("data"):
        os.makedirs("data")

    df = yf.Ticker(ticker).history(period=period)

    csv_path = f"data/{ticker}.csv"
    df.to_csv(csv_path)

    return df
    
