from typing import Optional


class AddProducerUsecase:
    def __init__(self, producer: Producer):
        self.producer = producer

    def execute(
        self, 
        user_id: str, 
        data: str, 
        run_id: Optional[str] = None,
        metadata: Optional[dict] = None
    ):
        self.producer.add(user_id, data, run_id, metadata)
