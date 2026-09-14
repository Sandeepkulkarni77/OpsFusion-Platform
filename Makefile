build:
	docker build -t opsfusion-api:1.0.0 .

run:
	docker run -d --name opsfusion-api -p 8000:8000 opsfusion-api:1.0.0

stop:
	docker stop opsfusion-api
	docker rm opsfusion-api
