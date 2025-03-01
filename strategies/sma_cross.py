import backtrader as bt

class SMACrossover(bt.Strategy):
    params = (('fast', 10), ('slow', 50))

    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=self.p.fast)
        self.sma_slow = bt.indicators.SMA(period=self.p.slow)
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        #
        cash = self.broker.getcash()
        # tweak this value to decide how much cash allocated for each trade, increasing => more risk & potentially reward and vice versa 
        risk_per_trade = cash * 0.50
        size = risk_per_trade // self.data.close[0]

        if not self.position:
            if self.crossover > 0:
                # buy signal
                self.buy(size=size)
                # putting stop-loss on entry price for each trade, means if stock falls beow this %age, exit and book losses
                self.stop_loss_price = self.data.close[0] * 0.40
        else:
            if self.data.close[0] < self.stop_loss_price:
                # Exit position if price falls below stop-loss
                self.close()

        # sell signal
            elif self.crossover < 0:
                self.close()