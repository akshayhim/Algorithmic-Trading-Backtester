import os
import csv
import backtrader as bt
import data_loader
from strategies.sma_cross import SMACrossover
from strategies.rsi_strategy import RSIStrategy
from strategies.bollinger_strategy import BollingerStrategy
from strategies.multi_signal_strategy import MultiSignalStrategy
from datetime import datetime

# Initialize Cerebro engine
cerebro = bt.Cerebro()

# Load data
data = bt.feeds.PandasData(dataname=data_loader.fetch_data())
cerebro.adddata(data)

# Choose strategy (SMACrossover, RSIStrategy, BollingerStrategy, or MultiSignalStrategy)
cerebro.addstrategy(MultiSignalStrategy)

# Set initial portfolio cash
cerebro.broker.set_cash(10000)

# Set brokerage commission
cerebro.broker.setcommission(commission=0.001)

# Adding analyzers for performance metrics
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

print("Project by Akshay Himatsingka akshayhimat@gmail.com")

#  Starting portfolio value
print("\nStarting Portfolio Value: %.2f" % cerebro.broker.getvalue())
init_portfolio = cerebro.broker.getvalue()

results = cerebro.run()

# Final portfolio value
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
end_portfolio = cerebro.broker.getvalue()

strat = results[0]

# Code section for printing performance metrics
#####################################################################
print("\nPerformance Metrics:")

# Total Return
total_return = ((end_portfolio - init_portfolio) / init_portfolio) * 100
print(f"Total Return: {total_return:.2f}%")


# Extracting integer part from period #
number = int(data_loader.period[0])
unit = data_loader.period[1]
if unit == 'y':
    period_reciprocal = 1 / number
elif unit == 'm':
    period_reciprocal = 1 / (number / 12)
#######################################

# Annualized Return
annualized_return = ((end_portfolio / init_portfolio) ** period_reciprocal) - 1
print(f"Annualized Return: {annualized_return * 100:.2f}%")

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

# Code section for creating and storing trade analysis in a separate file
#####################################################################
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