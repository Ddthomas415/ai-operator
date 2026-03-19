import numpy as np
import pandas as pd

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build light features from OHLCV (no extra deps)."""
    df = df.copy()
    # Basic returns
    df["ret_1"]  = df["close"].pct_change()
    df["ret_5"]  = df["close"].pct_change(5)
    df["ret_20"] = df["close"].pct_change(20)

    # Volatility
    df["vol_10"] = df["ret_1"].rolling(10).std()

    # EMAs
    df["ema_12"] = df["close"].ewm(span=12).mean()
    df["ema_26"] = df["close"].ewm(span=26).mean()
    df["ema_diff"] = (df["ema_12"] - df["ema_26"]) / df["close"]

    # Volume signal
    if "volume" in df.columns:
        df["vol_z"] = (df["volume"] - df["volume"].rolling(20).mean()) / (df["volume"].rolling(20).std() + 1e-9)
    else:
        df["vol_z"] = 0.0

    feats = df[[
        "ret_1", "ret_5", "ret_20",
        "vol_10", "ema_diff", "vol_z"
    ]].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return feats
