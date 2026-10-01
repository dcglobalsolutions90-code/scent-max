# Kalshi BTC 15m Paper Bot

Paper-only 1-second dashboard for Kalshi series `KXBTC15M`.

## Live data
- Discovers the active KXBTC15M market from Kalshi public market data.
- Refreshes the current market once per second.
- Displays YES/NO bid/ask, target, countdown, and automatically rolls to the next 15-minute contract.
- Uses a live BTC/USDT stream only as a reference signal. Kalshi's published settlement source controls the real market outcome.

## Paper engine
- YES or NO simulated positions only.
- Auto mode starts enabled.
- Enters when the internal fair-probability estimate differs from the executable Kalshi ask by at least 5.5 cents.
- Targets small paper wins of about 4 cents per contract.
- Paper stop at about 6 cents per contract.
- Blocks new entries in the final 25 seconds.
- No Kalshi account, API key, or real order submission.

## Settlement note
KXBTC15M market rules use the applicable CF Benchmarks Bitcoin reference methodology. The app's BTC stream is not the settlement oracle.
