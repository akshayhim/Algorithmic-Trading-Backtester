import backtrader as bt
from strategies.sma_cross import SMACrossover
import data_loader

if __name__ == "__main__":
    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(dataname=data_loader.fetch_data())
    cerebro.adddata(data)

    cerebro.addstrategy(SMACrossover, fast=5, slow=20)

    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.0001)

    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

    cerebro.optreturn = False
    results = cerebro.run()

    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    cerebro.plot()