from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional


class EventType(Enum):
    """Enumeration of possible solver step events."""

    VERTEX_LABELED = auto()
    EDGE_WEIGHT_CALCULATED = auto()
    BACKTRACK = auto()
    SOLUTION_FOUND = auto()


@dataclass(slots=True)
class StepEvent:
    """Structured data emitted by solvers to drive animations.

    Attributes
    ----------
    type:
        Category of the event (see :class:`EventType`).
    data:
        Arbitrary payload associated with the event. Recommended keys:
            - ``vertex``: The vertex being labeled or backtracked.
            - ``label``: Assigned label value (if applicable).
            - ``neighbor`` / ``edge``: Neighbor vertex or edge tuple.
            - ``weight``: Calculated edge weight.
    timestamp:
        Optional float seconds since epoch (can be filled by emitter).
    """

    type: EventType
    data: Dict[str, Any]
    timestamp: Optional[float] = None 