from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Vertex:
    system_id: str
    data: str
    data_type: str  # matched to neo4j entity type
    embedding: List[float]

    metadata: Dict

    def __str__(self) -> str:
        pretty = f"system_id={self.system_id}"
        pretty += f" data={self.data}"
        pretty += f" data_type={self.data_type}"
        pretty += f" metadata={self.metadata}"
        return pretty


@dataclass
class Edge:
    system_id: str
    data: str
    data_type: str  # matched to neo4j edge type
    source: Vertex
    target: Vertex
    metadata: Dict

    def __str__(self) -> str:
        pretty = f"system_id={self.system_id}"
        pretty += f" data={self.data}"
        pretty += f" data_type={self.data_type}"
        pretty += f" source={str(self.source)}"
        pretty += f" target={str(self.target)}"
        pretty += f" metadata={self.metadata}"
        return pretty
