run-api:
	poetry run uvicorn knowledge_base.app.api.main:app --port 3000 --reload

run-add-consumer:
	poetry run python -m knowledge_base.app.add_consumer.main
