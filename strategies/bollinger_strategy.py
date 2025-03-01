import backtrader as bt

class BollingerStrategy(bt.Strategy):
    params = (
        ('bb_period', 20),
    )

    def __init__(self):
        self.bb = bt.indicators.BollingerBands(self.data.close, period=self.params.bb_period)

    def next(self):
        if not self.position:
            if self.data.close[0] < self.bb.lines.bot[0]:
                self.buy()
                # stop-loss for each trade. If stock falls beow this %age of entry price, exit and book losses               
                self.stop_loss_price = self.data.close[0] * 0.90

        else:
            # Close position if price falls below stop-loss
            if self.data.close[0] < self.stop_loss_price:
                self.close()

            # Close Signal based on indicator trigger
            elif self.data.close[0] > self.bb.lines.top[0]:
                self.close()