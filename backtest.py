import os
import csv
import backtrader as bt
from strategies.sma_cross import SMACrossover
from strategies.rsi_strategy import RSIStrategy
from strategies.bollinger_strategy import BollingerStrategy
from strategies.multi_signal_strategy import MultiSignalStrategy
import data_loader
from datetime import datetime

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname=data_loader.fetch_data())
cerebro.adddata(data)

# Choose out of the 3 indicators (SMA, RSI, Bollinger Bands) or follow a multi signal strategy which combines the 3 indicators and triggers trade signal based on cocnditions set in the strategy file
cerebro.addstrategy(MultiSignalStrategy)

cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')

# tweak to allocate initial portfolio cash for trading
cerebro.broker.set_cash(10000)

# tweak to adjust for borkerage comission in %age 
cerebro.broker.setcommission(commission=0.001)

print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

results = cerebro.run()

print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

# code section for creating and storing trade analysis in sepearate file
#####################################################################
strat = results[0]
trade_analysis = strat.analyzers.trade_analyzer.get_analysis()

output_folder = "trade_analysis_results"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"{output_folder}/{data_loader.ticker}_{timestamp}.csv"

with open(filename, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)

    # Write header row for trade analysis
    writer.writerow(["Metric", "Value"])

    # Write trade analysis data (flatten dictionary)
    writer.writerow(["Trade Analysis", ""])
    for key, value in trade_analysis.items():
        if isinstance(value, dict):  # Nested dictionary handling
            for sub_key, sub_value in value.items():
                writer.writerow([f"{key} - {sub_key}", sub_value])
        else:
            writer.writerow([key, value])

print(f"Analysis saved to {filename}")
#####################################################################

cerebro.plot()