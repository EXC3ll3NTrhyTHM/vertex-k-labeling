from typing import List
from src.events import StepEvent

class EventRecorder:
    """Records StepEvent instances into a provided buffer list."""
    def __init__(self, buffer: List[StepEvent]) -> None:
        self.buffer = buffer

    def __call__(self, event: StepEvent) -> None:
        self.buffer.append(event)

__all__ = ["EventRecorder"] 