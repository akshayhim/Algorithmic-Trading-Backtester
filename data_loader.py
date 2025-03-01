import yfinance as yf

def fetch_data(ticker="HDFCBANK.NS", period="5y"):
    """fetch historical data"""
    df = yf.Ticker(ticker).history(period=period)
    df.to_csv(f"data/{ticker}.csv")
    return df
    
