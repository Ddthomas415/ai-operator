import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# make project root importable
sys.path.append(str(Path(__file__).resolve().parents[0].parents[0]))

from ai_engine.features import make_features
from ai_engine.model import LinearPolicy
from bot.broker import Broker

STORAGE = Path(__file__).resolve().parents[1] / "storage"
MODEL_PATH = STORAGE / "ai_model.pkl"

def backtest_episode(df: pd.DataFrame, policy: LinearPolicy, trade_qty: float = 1.0, txn_cost_bp: float = 2.0):
    """
    One pass over data to produce rewards and allow learning online.
    txn_cost_bp: round-trip cost in basis points (~0.02% default)
    """
    feats = make_features(df)
    rewards = []
    position = 0   # -1 short, 0 flat, +1 long (we'll keep it flat/long only for simplicity)
    entry_price = None
    cost = txn_cost_bp / 10000.0

    closes = df["close"].values
    for i in range(1, len(df)):
        x = feats.iloc[i].values.astype(float)
        act = policy.act(x)  # -1,0,1 (we'll map -1 -> close long if any)

        reward = 0.0
        price = float(closes[i])
        prev  = float(closes[i-1])

        # PnL on holding position
        if position == 1:
            reward += (price - prev) / prev

        # Execute action (simple: 1=open/keep long, -1=exit to flat)
        if act == 1 and position == 0:
            # enter long (pay cost)
            position = 1
            entry_price = price
            reward -= cost
        elif act == -1 and position == 1:
            # exit long (pay cost)
            position = 0
            reward -= cost
            entry_price = None

        # Update policy with obtained reward signal (scaled)
        policy.update_sgd(x, reward, lr=0.01)
        rewards.append(reward)

    # final exit cost if still long at end (optional)
    if position == 1:
        rewards[-1] -= cost

    return float(np.sum(rewards)), float(np.mean(rewards)), float(np.std(rewards) + 1e-12)

def train_once(symbol: str = "BTC/USDT", timeframe: str = "1h", bars: int = 500):
    broker = Broker(exchange_id="coinbasepro", mode=os.getenv("TRADING_MODE", "paper"))
    df = broker.fetch_ohlcv(symbol, timeframe, limit=bars).dropna()
    if len(df) < 50:
        raise RuntimeError("Not enough data to train.")

    feats = make_features(df)
    policy = LinearPolicy(n_features=feats.shape[1])

    total, avg, vol = backtest_episode(df, policy)

    # light threshold tuning
    # set buy/sell thresholds around average score/std of projections
    proj = np.dot(feats.values, policy.w)
    if np.std(proj) > 1e-6:
        policy.buy_th  = float(np.percentile(proj, 65))
        policy.sell_th = float(np.percentile(proj, 35)) * 0.0 - abs(policy.buy_th)  # symmetric-ish
    policy.save(str(MODEL_PATH))
    return {
        "model_path": str(MODEL_PATH),
        "reward_total": total,
        "reward_avg": avg,
        "reward_vol": vol,
        "bars": int(len(df)),
        "symbol": symbol,
        "timeframe": timeframe
    }

if __name__ == "__main__":
    info = train_once()
    print("✅ Trained:", info)
