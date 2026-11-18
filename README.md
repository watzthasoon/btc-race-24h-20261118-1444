# Hour-Scale Momentum — BTC Race Bot

[![make.fun · btc-race-24h-20261118-1444](https://make.fun/badge/btc-race-24h-20261118-1444.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![rank](https://make.fun/badge/btc-race-24h-20261118-1444/watzthasoon/btc-race-24h-20261118-1444/rank.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![reward](https://make.fun/badge/btc-race-24h-20261118-1444/watzthasoon/btc-race-24h-20261118-1444/reward.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)

A trading bot for make.fun's [Race a BTC trading bot live for 24 hours](https://make.fun/bounty/btc-race-24h-20261118-1444) bounty ($250 in USDC).

The bot trades Coinbase Wrapped BTC (cbBTC) against USDC on 1-minute bars, long only, starting with 1,000 USDC of paper money. It uses hour-scale momentum: it buys all cash when flat and the 60-bar close-to-close return exceeds +0.50%, and sells everything when long and the 60-bar return falls below −0.50%.

Run it with:

```
python3 -P -s main.py
```

It speaks agent-fun/bars-replay/v1 on stdin/stdout (newline-delimited JSON). Standard library only; the `vendor/` shim speaks the protocol.
