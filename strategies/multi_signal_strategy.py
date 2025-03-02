import backtrader as bt

class MultiSignalStrategy(bt.Strategy):
    params = (
        ('fast', 18),         # Fast SMA period
        ('slow', 50),         # Slow SMA period
        ('rsi_period', 15),   # RSI period
        ('rsi_lower', 30),    # RSI oversold threshold
        ('rsi_upper', 67),    # RSI overbought threshold
        ('bb_period', 27),    # Bollinger Bands period
    )

    def __init__(self):
        self.sma_fast = bt.indicators.SMA(self.data.close, period=self.params.fast)
        self.sma_slow = bt.indicators.SMA(self.data.close, period=self.params.slow)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.bb = bt.indicators.BollingerBands(self.data.close, period=self.params.bb_period)

    def next(self):
        if not self.position:
            buy_signals = sum([
                self.sma_fast[0] > self.sma_slow[0],          
                self.rsi[0] < self.params.rsi_lower,          
                self.data.close[0] < self.bb.lines.bot[0],    
            ])

            # Buy if at least 1 out of the 3 signals is/are true (lower num = more aggressive, higher num = more conservative)
            if buy_signals >= 1:
                self.buy()

                # Stop-loss for each trade. If stock falls beow this %age of entry price, exit and book losses               
                self.stop_loss_price = self.data.close[0] * 0.87

        else:
            # Close position if price falls below stop-loss
            if self.data.close[0] < self.stop_loss_price:
                  self.close()

            # Close Signal
            sell_signals = sum([
                self.sma_fast[0] < self.sma_slow[0],          
                self.rsi[0] > self.params.rsi_upper,         
                self.data.close[0] > self.bb.lines.top[0], 
            ])

            # Sell if at least 3 out of 3 signals is/are true (lower num = more conservative, higher num = more aggressive)
            if sell_signals >= 3:
                self.close()