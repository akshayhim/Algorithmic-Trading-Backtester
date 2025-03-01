
from backtrader import Cerebro
from strategies.sma_cross import SMACrossover
import data_loader

cerebro = Cerebro()

data = bt.feeds.PandasData(dataname=data_loader.fetch_data())
cerebro.adddata(data)

cerebro.addstrategy(SMACrossover)

print("Strating Portfolio Value: %.2f" % cerebro.broker.getValue())
results = cerebro.run()
print("Final Portfolio Value: %.2f" % cerebro.broker.getValue())

cerebro.plot()