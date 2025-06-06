# 💹 Custom Binance Strategy Backtest (Backtrader + yFinance)

This repository contains a backtesting implementation of a custom Binance-style trading strategy using the [Backtrader](https://www.backtrader.com/) framework and historical Bitcoin (BTC-USD) data from [Yahoo Finance](https://finance.yahoo.com/).

---

## 📈 Strategy Overview

The strategy is inspired by modern crypto momentum and oscillator-based techniques. It uses a combination of:

- **Relative Strength Index (RSI)** – for overbought/oversold signals
- **Exponential Moving Averages (EMA 8 and EMA 16)** – to identify bullish/bearish price movement
- **Stochastic Fast Oscillator** – to detect strong short-term reversals
- **CTI (Custom Trend Indicator)** – a custom implementation for short-term trend reversion
- **EWO (Elliott Wave Oscillator)** – measures momentum based on difference between EMAs
- **Simple Moving Average (SMA 15)** – trend-following confirmation

### 🔍 Buy Conditions
The strategy evaluates two primary sets of conditions before entering a trade:

#### 1. **EWO Momentum Entry**
- RSI (Fast) < 50
- Price below EMA8 * 0.956
- EWO > -1.238
- Price below EMA16 * 0.986
- RSI (14) < 30

#### 2. **Oversold Reversion Entry**
- RSI (20) is decreasing
- RSI (Fast) < 63
- RSI (14) > 16
- Price below SMA15 * 0.932
- CTI < -0.8

### 💰 Sell Condition
- **Stochastic Fast %K > 75** – suggesting price has potentially topped out in the short term

---

## 📊 Backtest Results

**Period:** 721 days  
**Data Source:** Yahoo Finance (BTC-USD)  
**Initial Capital:** $10,000  
**Position Sizing:** 95% of available cash per trade  
**Commission:** 0.1% per trade

| Metric                  | Value       |
|-------------------------|-------------|
| Final Portfolio Value   | $13,266.99  |
| Total Return            | **+32.67%** |
| Total Trades Executed   | 4           |
| Win Rate                | **100%**    |
| Sharpe Ratio            | 1.16        |
| Max Drawdown            | **4.01%**   |

---

