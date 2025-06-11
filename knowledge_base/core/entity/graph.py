from dataclasses import dataclass
from typing import Dict


@dataclass
class Vertex:
    system_id: str
    data: str
    data_type: str
    embedding: list[float] | None = None

    metadata: Dict | None = None


@dataclass
class Edge:
    system_id: str
    data: str
    embedding: list[float] | None = None

    source: Vertex
    target: Vertex
    metadata: Dict | None = None
