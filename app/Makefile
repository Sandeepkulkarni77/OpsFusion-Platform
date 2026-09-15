.PHONY: install run docker-build docker-run

install:
	pip install -r requirements.txt

run:
	python app.py

docker-build:
	docker build -t opsfusion-api:0.1.0 .

docker-run:
	docker run --rm -p 8000:8000 opsfusion-api:0.1.0
