from dataclasses import dataclass
from typing import List, Dict
from knowledge_base.core.entity.graph import Edge


@dataclass
class KnowledgeSource:
    system_id: str
    data: str
    metadata: Dict


@dataclass
class Knowledge:
    system_id: str
    edges: List[Edge]
