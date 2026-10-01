# WLFI AI Paper Trader

Paper-only trading bot for **WLFI/USDT**.

## Current mode

- No API keys
- No account access
- No real orders
- Live public WLFI/USDT market data
- Simulated paper fills and fees
- Local paper account state on the device

## Signal model

The browser strategy combines:

1. EMA 9 / EMA 21 trend
2. RSI 14
3. MACD 12 / 26 momentum
4. Bollinger Band position
5. Short momentum
6. Volume impulse

The six factors generate a score from -100 to +100.

## Risk engine

- Configurable risk per trade
- Configurable maximum allocation
- ATR-based initial stop
- Reward/risk take-profit
- Break-even / trailing stop logic
- Daily loss guard
- Paper fees
- Spot-long paper positions only

## Backtest

The app retrieves historical candles and simulates the same rules with fees. This is for strategy research only and does not imply future performance.

## Important PWA limitation

The browser bot runs while the page/PWA is active. iOS can suspend JavaScript when an app is backgrounded or the phone sleeps. A later server-side paper-trading engine is required for reliable 24/7 unattended execution.
