import backtrader as bt

class SMACrossover(bt.Strategy):
    params = (('fast', 10), ('slow', 50))

    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=self.p.fast)
        self.sma_slow = bt.indicators.SMA(period=self.p.slow)
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                # buy signal
                self.buy()
                # stop-loss for each trade. If stock falls beow this %age of entry price, exit and book losses
                self.stop_loss_price = self.data.close[0] * 0.90
        else:
            # Close position if price falls below stop-loss
            if self.data.close[0] < self.stop_loss_price:
                self.close()

            # Close Signal based on indicator trigger
            elif self.crossover < 0:
                self.close()