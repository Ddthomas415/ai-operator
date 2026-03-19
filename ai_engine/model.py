import pickle
import numpy as np

class LinearPolicy:
    """
    Simple linear policy:
      action_score = w · x
      trade when score crosses thresholds.
    Actions: -1 (sell), 0 (hold), +1 (buy)
    """

    def __init__(self, n_features: int, seed: int = 42):
        rng = np.random.RandomState(seed)
        self.w = rng.normal(0, 0.05, size=(n_features,))
        self.buy_th =  0.15   # thresholds can be tuned by trainer
        self.sell_th = -0.15

    def act(self, x: np.ndarray) -> int:
        s = float(np.dot(self.w, x))
        if s >= self.buy_th:
            return 1
        elif s <= self.sell_th:
            return -1
        return 0

    def update_sgd(self, x: np.ndarray, reward: float, lr: float = 0.01):
        # Policy gradient lite: push weights in direction of reward * gradient
        # gradient of score w.r.t w is x, use reward-scaled update
        self.w += lr * reward * x

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump({
                "w": self.w,
                "buy_th": self.buy_th,
                "sell_th": self.sell_th
            }, f)

    @classmethod
    def load(cls, path: str):
        with open(path, "rb") as f:
            state = pickle.load(f)
        obj = cls(n_features=len(state["w"]))
        obj.w = state["w"]
        obj.buy_th = state["buy_th"]
        obj.sell_th = state["sell_th"]
        return obj
