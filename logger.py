import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/events.jsonl")

def log_event(input_text: str, action: str, confidence: float, result: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "input": input_text,
        "action": action,
        "confidence": confidence,
        "result": result,
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
