database:
	docker-compose up -d

dev:
	uv run uvicorn src.main:app --reload