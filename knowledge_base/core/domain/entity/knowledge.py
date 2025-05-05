from typing import TypedDict, Optional


class Knowledge(TypedDict):
    id: str
    user_id: str
    run_id: Optional[str]
    data: str
    metadata: dict
