"""Hour-scale momentum bot for CBBTC/USDC, agent-fun/bars-replay/v1.

Strategy (original design, written for this competition):

1-minute bars of wrapped BTC are dominated by noise: on the dev window a
1-minute EMA crossover whipsaws dozens of times and loses far more to the
~26 bps full round-trip cost than it gains. What survives the costs is the
slower, hour-scale drift: the dev window falls ~2.8% overall but recovers
in a sustained multi-hour leg in the middle, and a 60-minute return filter
catches that leg while sitting in cash through the chop.

Rule, evaluated on each bar's close (decision at bar k fills at bar k+1's
open, so every signal is one bar late by construction):
  - Flat and the 60-bar close-to-close return exceeds +0.50%  -> buy, all cash.
  - Long and the 60-bar return falls below -0.50%            -> sell everything.
  - Otherwise hold (cash or position).

The thresholds are symmetric (+/-0.50%) and the window is one hour: a
round trip must clear ~26 bps of fee + slippage + impact, so a 50 bps
signal leaves room for the fill lag and the costs. The bot holds at most
one position, never shorts, uses no leverage, and trades at most twice
per signal change, so drawdown stays small. Fully deterministic: no
randomness, no clock, no files, no network; the only state is the list of
closes seen so far.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

SYMBOL = "CBBTC"

# 60 one-minute bars = one hour of returns.
LOOKBACK = 60
# Entry/exit thresholds on the 60-bar return, in basis points.
ENTRY_BPS = 50
EXIT_BPS = -50
# Max slippage vs the latest close, in bps. A fill pays ~2 bps modelled
# slippage plus ~10 bps impact at full size, and a 1-minute open rarely
# moves far from the prior close; 200 bps only rejects a true gap.
MAX_SLIPPAGE_BPS = 200

# Closes (integer price units) in the order received.
_closes = []


def _return_bps():
    """60-bar close-to-close return in bps, or None before enough history."""
    if len(_closes) <= LOOKBACK:
        return None
    now = _closes[-1]
    then = _closes[-1 - LOOKBACK]
    if then <= 0:
        return None
    return (now - then) * 10_000 // then


def on_batch(state, batch):
    bar = state.latest.get(SYMBOL)
    if bar is not None:
        _closes.append(int(bar["c"]))
    if state.warming_up:
        return []
    ret = _return_bps()
    if ret is None:
        return []
    holding = state.positions.get(SYMBOL)
    if holding is None:
        if ret > ENTRY_BPS:
            cash = state.cash
            room = state.weight_room(SYMBOL)
            amount = cash if cash < room else room
            if amount >= 1_000_000:  # min notional: 1 USDC
                return [{
                    "side": "buy",
                    "symbol": SYMBOL,
                    "notional_quote_units": amount,
                    "max_slippage_bps": MAX_SLIPPAGE_BPS,
                }]
        return []
    if ret < EXIT_BPS:
        qty = holding.qty
        if qty > 0 and state.value(SYMBOL, qty) >= 1_000_000:
            return [{
                "side": "sell",
                "symbol": SYMBOL,
                "qty": qty,
                "max_slippage_bps": MAX_SLIPPAGE_BPS,
            }]
    return []


makefun_bars.run(on_batch)
