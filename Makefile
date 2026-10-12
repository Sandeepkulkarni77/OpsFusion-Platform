.PHONY: db-start db-migrate deploy status logs stop build test lint

db-start:
	docker compose up -d db

db-migrate:
	docker compose run --rm api1 flask --app app db upgrade

deploy:
	docker compose up -d db
	@until [ "$$(docker inspect -f '{{.State.Health.Status}}' "$$(docker compose ps -q db)")" = "healthy" ]; do sleep 2; done
	docker compose run --rm api1 flask --app app db upgrade
	docker compose up -d --build api1 api2 nginx

status:
	docker compose ps

logs:
	docker compose logs --tail=100 -f

stop:
	docker compose down

build:
	python3 -m venv .venv
	.venv/bin/python -m pip install -r app/requirements.txt

test:
	.venv/bin/python -m unittest discover -s app -p "test_*.py"

lint:
	ruff check app
