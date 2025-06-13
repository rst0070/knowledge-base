from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Vertex:
    system_id: str
    data: str
    data_type: str  # matched to neo4j entity type
    embedding: List[float]

    metadata: Dict


@dataclass
class Edge:
    system_id: str
    data: str  # matched to neo4j edge type

    source: Vertex
    target: Vertex
    metadata: Dict
