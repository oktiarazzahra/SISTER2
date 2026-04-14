from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Node:
    name: str
    x: float
    y: float
    color: str
    radius: int = 28


@dataclass
class Packet:
    msg_id: int
    model: str
    phase: str
    kind: str
    path: List[Tuple[float, float]]
    speed: float
    created_at: float
    dropped: bool = False
    progress: float = 0.0
