run-api:
	poetry run uvicorn knowledge_base.app.api.main:app --port 3000 --reload

run-add-consumer:
	poetry run python -m knowledge_base.present.add_consumer.main

run-mcp:
	poetry run mcp run --port 3000 --reload