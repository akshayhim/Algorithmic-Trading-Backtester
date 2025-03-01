# Algorithmic Trading Backtester

A backtesting framework for algorithmic trading strategies that supports various indicators such as SMA, RSI, and Bollinger Bands. The framework also allows combining the strengths of all three indicators to generate multi-signal strategies and evaluate their performance on historical stock price data. Users can adjust risk exposure through cash allocation and stop-loss mechanisms, optimize parameters, and analyze performance metrics.

## Features

- Backtest various trading strategies on any listed security of your choice
- Design highly customized and personalized trading setup tailored to your preferences and risk tolerance
- Analyze detailed csv reports for each backtest, containing comprehensive information about every trade
- Adjust risk management settings with flexible cash allocation and stop-loss mechanisms
- Modular framework for easily adding new indicators to expand functionality

## Installation

Clone the repository:

```bash
git clone https://github.com/akshayhim/Algorithmic-Trading-Backtester
```

Navigate to the project directory:

```bash
cd algorithmic-trading-backtester
```

Set up a python virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate (Mac/Linux)
venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

Basic run setup:

```bash
go to data_loader.py
change 'ticker' to your choice of stock's ticker on https://finance.yahoo.com/
change period to your choice (1m, 3y, 5y, etc)

go to backtest.py
change cerebro.addstrategy() to the indicator of your choice
```

Run Command (make sure you're in root directory):

```bash
python backtest.py
```

View performance metrics and detialed analysis in the terminal and the generated CSV files respectively.

## Project Structure

algorithmic-trading-backtester/
├── strategies/
│ ├── sma_strategy.py # SMA strategy logic
│ ├── rsi_strategy.py # RSI strategy logic
│ ├── bollinger_strategy.py # Bollinger Bands strategy logic
│ └── multi_signal_strategy.py # Multi-signal strategy combining all indicators
├── data_loader.py # Fetches historical stock data
├── backtest.py # Main script to run backtests
├── requirements.txt # Python dependencies
└── README.md # Project documentation

## Screenshots

![backtest chart](screenshots/combinedss.png)
