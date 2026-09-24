.PHONY: db-start db-migrate api-build api-run

db-start:
	docker compose up -d db

db-migrate:
	docker compose run --rm api flask db upgrade

api-build:
	docker compose build api

api-run:
	$(MAKE) db-start
	$(MAKE) db-migrate
	docker compose up -d api
