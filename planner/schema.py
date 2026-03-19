from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ActionStep:
    step_input: str
    action: str
    confidence: float
    clarification_needed: bool
    clarification_question: str | None
    reason: str
    filename: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ActionPlan:
    original_input: str
    steps: list[ActionStep]

    def to_dict(self) -> dict[str, Any]:
        return {
            "original_input": self.original_input,
            "steps": [step.to_dict() for step in self.steps],
        }
