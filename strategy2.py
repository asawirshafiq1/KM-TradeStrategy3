import backtrader as bt
import datetime
import yfinance as yf


class CustomBinanceStrategy(bt.Strategy):
    params = dict(
        buy_rsi_fast=50,
        buy_rsi=30,
        buy_ewo=-1.238,
        buy_ema_low=0.956,
        buy_ema_high=0.986,
        buy_rsi_fast_32=63,
        buy_rsi_32=16,
        buy_sma15_32=0.932,
        buy_cti_32=-0.8,
        sell_fastx=75,
        order_pct=0.95,
    )

    def __init__(self):
        self.ema_8 = bt.ind.EMA(self.data.close, period=8)
        self.ema_16 = bt.ind.EMA(self.data.close, period=16)
        self.rsi = bt.ind.RSI(self.data.close, period=14)
        self.rsi_fast = bt.ind.RSI(self.data.close, period=4)
        self.rsi_slow = bt.ind.RSI(self.data.close, period=20)
        self.sma_15 = bt.ind.SMA(self.data.close, period=15)
        self.cti = (self.data.close - self.data.close(-1)) / self.data.close
        self.ewo = (bt.ind.EMA(self.data.close, period=50) - bt.ind.EMA(self.data.close, period=200)) / self.data.low * 100
        stoch = bt.ind.StochasticFast(self.data, period=5, period_dfast=3)
        self.fastk = stoch.percK
        self.fastd = stoch.percD


    def next(self):
        if not self.position:
            is_ewo = (
                self.rsi_fast[0] < self.p.buy_rsi_fast and
                self.data.close[0] < self.ema_8[0] * self.p.buy_ema_low and
                self.ewo[0] > self.p.buy_ewo and
                self.data.close[0] < self.ema_16[0] * self.p.buy_ema_high and
                self.rsi[0] < self.p.buy_rsi
            )

            buy_1 = (
                self.rsi_slow[0] < self.rsi_slow[-1] and
                self.rsi_fast[0] < self.p.buy_rsi_fast_32 and
                self.rsi[0] > self.p.buy_rsi_32 and
                self.data.close[0] < self.sma_15[0] * self.p.buy_sma15_32 and
                self.cti[0] < self.p.buy_cti_32
            )

            if is_ewo or buy_1:
                cash = self.broker.get_cash()
                size = (cash * self.p.order_pct) / self.data.close[0]
                self.buy(size=size)
        else:
            if self.fastk[0] > self.p.sell_fastx:
                self.close()


def run_strategy():
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=720)

    print(f"Downloading BTC data from {start_date.date()} to {end_date.date()}")
    btc_df = yf.download('BTC-USD', start=start_date, end=end_date, auto_adjust=False)

    if btc_df.columns.nlevels > 1:
        btc_df.columns = btc_df.columns.get_level_values(0)

    btc_df = btc_df[['Open', 'High', 'Low', 'Close', 'Volume']]
    btc_df.dropna(inplace=True)

    print(f"Data loaded: {btc_df.shape[0]} days")

    data = bt.feeds.PandasData(dataname=btc_df)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(CustomBinanceStrategy)
    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.001)

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    print(f'\nStarting Portfolio Value: ${cerebro.broker.getvalue():.2f}')
    results = cerebro.run()
    strat = results[0]
    final_value = cerebro.broker.getvalue()
    print(f'Final Portfolio Value: ${final_value:.2f}')
    print(f'Total Return: {((final_value - 10000) / 10000) * 100:.2f}%')

    trades = strat.analyzers.trades.get_analysis()
    if 'total' in trades:
        total = trades.total.total
        wins = trades.won.total if 'won' in trades else 0
        losses = trades.lost.total if 'lost' in trades else 0
        win_rate = (wins / total * 100) if total > 0 else 0
        print(f"\nTotal Trades: {total}, Win Rate: {win_rate:.2f}%")

    sharpe = strat.analyzers.sharpe.get_analysis()
    if sharpe.get('sharperatio'):
        print(f"Sharpe Ratio: {sharpe['sharperatio']:.2f}")

    drawdown = strat.analyzers.drawdown.get_analysis()
    if drawdown.get('max'):
        print(f"Max Drawdown: {drawdown['max']['drawdown']:.2f}%")

    cerebro.plot(style='candlestick')


if __name__ == '__main__':
    run_strategy()