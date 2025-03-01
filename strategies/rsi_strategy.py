import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = {
        ('rsi_period', 14),
        ('rsi_lower', 30),
        ('rsi_upper', 70),
    }

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

    def next(self):
        cash = self.broker.getcash()
        # tweak to decide %age of cash allocated for each trade, increasing => more risk & potentially reward and vice versa 
        risk_per_trade = cash * 0.50
        size = risk_per_trade // self.data.close[0]

        if not self.position:
            # Buy Signal
            if self.rsi[0] < self.params.rsi_lower:
                self.buy(size=size)
                # stop-loss for each trade. If stock falls beow this %age of entry price, exit and book losses               
                self.stop_loss_price = self.data.close[0] * 0.90

        else:
            # Close position if price falls below stop-loss
            if self.data.close[0] < self.stop_loss_price:
                self.close()

            # Close Signal based on indicator trigger
            elif self.rsi[0] > self.params.rsi_upper:
                self.close()
    