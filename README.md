# OpsFusion-Platform
OpsFusion Platform is an end-to-end DevOps system that integrates CI/CD, containerization, Kubernetes orchestration, GitOps-based deployments, and observability into a unified automated workflow from development to production.

##  Architecture diagram

<img width="1056" height="705" alt="image" src="https://github.com/user-attachments/assets/da9ecfd5-790a-4339-9f4c-8fdc5be287bc" />


---

# Milestone 1 – REST API

The first milestone focuses on building a REST API for managing student records.

## Features

- Flask-based REST API
- Student CRUD operations
- Versioned API endpoints using `/api/v1`
- Health check endpoint
- SQLite database integration
- Environment-based configuration
- Application logging

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/healthcheck` | Check application health |
| POST | `/api/v1/students` | Create a student |
| GET | `/api/v1/students` | Get all students |
| GET | `/api/v1/students/<id>` | Get a student by ID |
| PUT | `/api/v1/students/<id>` | Update a student |
| DELETE | `/api/v1/students/<id>` | Delete a student |

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Sandeepkulkarni77/OpsFusion-Platform.git
cd OpsFusion-Platform
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r app/requirements.txt
```

### 4. Run the Application

```bash
cd app
python app.py
```

The application will be available at:

```text
http://localhost:8000
```

### 5. Verify Application Health

```bash
curl http://localhost:8000/healthcheck
```

Expected response:

```json
{
  "status": "ok"
}
```

## REST API Examples

### Create a Student

```bash
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Sandeep","email":"sandeep@example.com","age":22}'
```

### Get All Students

```bash
curl http://localhost:8000/api/v1/students
```

### Get Student by ID

```bash
curl http://localhost:8000/api/v1/students/1
```

### Update Student

```bash
curl -X PUT http://localhost:8000/api/v1/students/1 \
  -H "Content-Type: application/json" \
  -d '{"age":23}'
```

### Delete Student

```bash
curl -X DELETE http://localhost:8000/api/v1/students/1
```

---

# Milestone 2 – Containerization

The second milestone focuses on containerizing the REST API using Docker.

## What Was Implemented

- Created a Dockerfile for the Flask application
- Built a Docker image
- Ran the application inside a Docker container
- Exposed the application on port `8000`
- Verified the containerized application
- Added a Makefile for common Docker operations
- Added `.gitignore` for local and generated files

## Dockerfile

The application is packaged using a lightweight Python image.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

ENV PORT=8000

CMD ["python", "app.py"]
```

## Build the Docker Image

Run the following command from the project root:

```bash
docker build -t opsfusion-api:1.0.0 .
```

## Run the Docker Container

```bash
docker run -d \
  --name opsfusion-api \
  -p 8000:8000 \
  opsfusion-api:1.0.0
```

## Verify the Container

Check whether the container is running:

```bash
docker ps
```

Test the application:

```bash
curl http://localhost:8000/healthcheck
```

Expected response:

```json
{
  "status": "ok"
}
```

## View Container Logs

```bash
docker logs opsfusion-api
```

## Stop the Container

```bash
docker stop opsfusion-api
```

## Remove the Container

```bash
docker rm opsfusion-api
```

## Makefile

The project includes a Makefile to simplify commonly used Docker commands.

### Build

```bash
make build
```

### Run

```bash
make run
```

### Stop and Remove

```bash
make stop
```

---

# Project Structure

```text
OpsFusion-Platform/
│
├── app/
│   ├── app.py
│   └── requirements.txt
│
├── Dockerfile
├── Makefile
├── .gitignore
└── README.md
```

---
