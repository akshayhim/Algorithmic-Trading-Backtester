import os
import csv
import backtrader as bt
import data_loader
from strategies.sma_cross import SMACrossover
from strategies.rsi_strategy import RSIStrategy
from strategies.bollinger_strategy import BollingerStrategy
from strategies.multi_signal_strategy import MultiSignalStrategy
from datetime import datetime

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname=data_loader.fetch_data())
cerebro.adddata(data)

# Choose out of the 3 indicators (SMACrossover, RSIStrategy, BollingerStrategy) or follow a 'MultiSignalStrategy' which combines the 3 indicators and triggers trade signal based on cocnditions set in the strategy file
cerebro.addstrategy(MultiSignalStrategy)

# tweak to allocate initial portfolio cash for trading
cerebro.broker.set_cash(10000)

# tweak to adjust for borkerage comission in %age 
cerebro.broker.setcommission(commission=0.001)

# cerebro analyzers being added
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

print("Project by Akshay Himatsingka akshayhimat@gmail.com")

print("\nStarting Portfolio Value: %.2f" % cerebro.broker.getvalue())

results = cerebro.run()

print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())


# Accessing performance metrics
strat = results[0]

# code section for printing performance metrics
#####################################################################
print("\nPerformance Metrics:")
    
# Total Return
total_return = strat.analyzers.returns.get_analysis()['rtot']
print(f"Total Return: {total_return * 100:.2f}%")

# Annualized Return
annual_return = strat.analyzers.returns.get_analysis()['rnorm']
print(f"Annualized Return: {annual_return * 100:.2f}%")

# Sharpe Ratio
sharpe_ratio = strat.analyzers.sharpe.get_analysis()['sharperatio']
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# Maximum Drawdown
max_drawdown = strat.analyzers.drawdown.get_analysis()['max']['drawdown']
print(f"Maximum Drawdown: {max_drawdown:.2f}%")

# Trade Analysis
trade_analysis = strat.analyzers.trade_analyzer.get_analysis()
total_trades = trade_analysis.total.closed if 'closed' in trade_analysis.total else 0
win_rate = (trade_analysis.won.total / total_trades) * 100 if total_trades > 0 else 0

print(f"Total Trades: {total_trades}")
print(f"Win Rate: {win_rate:.2f}%")
#####################################################################


# code section for creating and storing trade analysis in sepearate file
#####################################################################
trade_analysis = strat.analyzers.trade_analyzer.get_analysis()

output_folder = "trade_analysis_results"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"{output_folder}/{data_loader.ticker}_{timestamp}.csv"

with open(filename, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(["Created by Akshay Himatsingka akshayhimat@gmail.com"])

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

print(f"\nDetailed Analysis saved to {filename}\n")
#####################################################################

cerebro.plot()