import os
import csv
import backtrader as bt
from strategies.sma_cross import SMACrossover
import data_loader
from datetime import datetime

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname=data_loader.fetch_data())
cerebro.adddata(data)

cerebro.addstrategy(SMACrossover, fast=5, slow=20)

cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
# cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

# tweak to allocate initial portfolio cash for trading
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

# cerebro.optreturn = False
results = cerebro.run()

print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

# trade analysis
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


cerebro.plot()

