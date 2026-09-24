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

# Milestone 3 – PostgreSQL, Docker Compose & Database Migrations

The third milestone focuses on replacing the local SQLite database with PostgreSQL and creating a reproducible local development environment using Docker Compose and Flask-Migrate.

## What Was Implemented

- Replaced SQLite with PostgreSQL for the containerized application
- Added PostgreSQL 16 as a Docker Compose service
- Added Docker Compose for running the API and database together
- Added environment-based database configuration
- Added Flask-SQLAlchemy PostgreSQL integration
- Added Flask-Migrate and Alembic for database migrations
- Created the initial `students` table migration
- Added migration files to version control
- Updated the API Dockerfile to include migrations
- Added Makefile commands for database startup, migrations, API builds and API startup
- Verified API-to-PostgreSQL connectivity
- Verified CRUD operations against PostgreSQL
- Added a one-command workflow to start the database, run migrations and start the API

## Architecture

The application now follows this architecture:

```text
                    ┌─────────────────────┐
                    │       Client        │
                    │       curl          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask REST API   │
                    │    API Container    │
                    └──────────┬──────────┘
                               │
                               │ SQL
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │    DB Container     │
                    └─────────────────────┘
```

---

## Docker Compose

The application now uses two services:

```text
API
 │
 └── PostgreSQL
```

The `docker-compose.yml` defines:

- `db` — PostgreSQL 16 database
- `api` — Flask REST API

The API connects to PostgreSQL using the `DATABASE_URL` environment variable.

```yaml
services:
  db:
    image: postgres:16
    env_file:
      - .env

  api:
    build:
      context: .
      dockerfile: app/Dockerfile
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```

---

## Environment Variables

Database credentials are stored locally in `.env` and are **not committed to Git**.

Example:

```env
POSTGRES_DB=opsfusion
POSTGRES_USER=opsfusion
POSTGRES_PASSWORD=localdevpassword
```

The `.env` file is included in `.gitignore`.

Verify that Git ignores the file:

```bash
git check-ignore -v .env
```

The password is therefore not stored directly in `docker-compose.yml` or committed to the repository.

---

# Database Migrations

Flask-Migrate and Alembic are used to manage database schema changes.

## Initialize Migrations

```bash
flask --app app.app db init
```

## Create a Migration

```bash
flask --app app.app db migrate -m "create students table"
```

## Apply Migrations

```bash
flask --app app.app db upgrade
```

The initial migration creates the `students` table.

Migration files are stored under:

```text
migrations/
├── README
├── alembic.ini
├── env.py
├── script.py.mako
└── versions/
    └── 714610d08115_create_students_table.py
```

---

# Makefile Commands

The Makefile was extended to simplify the development workflow.

## Start PostgreSQL

```bash
make db-start
```

This starts the PostgreSQL container.

## Run Database Migrations

```bash
make db-migrate
```

This runs the pending migrations against PostgreSQL.

## Build the API Image

```bash
make api-build
```

This builds the Flask API Docker image.

## Start the Complete Application

```bash
make api-run
```

The `api-run` target performs the following steps:

```text
Start PostgreSQL
      ↓
Run database migrations
      ↓
Start API
```

This provides a single command to start the complete local environment.

---

# Verify the Environment

## Check Running Containers

```bash
docker compose ps
```

Expected services:

```text
opsfusion-platform-api-1
opsfusion-platform-db-1
```

Both containers should show a running status.

---

# Verify API Health

```bash
curl http://localhost:8000/healthcheck
```

Expected response:

```json
{
  "status": "ok"
}
```

The health check executes a database query to verify that the API can communicate with PostgreSQL.

---

# Test Student Creation

Create a student:

```bash
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Sandeep","email":"sandeep@example.com","age":22}'
```

Expected response:

```json
{
  "age": 22,
  "email": "sandeep@example.com",
  "id": 1,
  "name": "Sandeep"
}
```

---

# Verify Data

Retrieve all students:

```bash
curl http://localhost:8000/api/v1/students
```

Example response:

```json
[
  {
    "age": 22,
    "email": "sandeep@example.com",
    "id": 1,
    "name": "Sandeep"
  }
]
```

This confirms that the API can successfully write to and read from PostgreSQL.

---

# Database Migration Workflow

When the database schema changes, the workflow is:

```text
Modify SQLAlchemy Model
          ↓
flask db migrate
          ↓
Migration File Created
          ↓
Review Migration
          ↓
flask db upgrade
          ↓
Database Schema Updated
```

Migration files are committed to Git so that other developers and environments can reproduce the same database schema.

---

# Current Project Structure

```text
OpsFusion-Platform/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── Makefile
│   └── requirements.txt
│
├── migrations/
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 714610d08115_create_students_table.py
│
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── .gitignore
└── README.md
```

---

# Development Workflow

The current recommended workflow is:

```bash
# Start the database, run migrations and start the API
make api-run
```

Verify the environment:

```bash
docker compose ps
```

Check API health:

```bash
curl http://localhost:8000/healthcheck
```

Test the API:

```bash
curl http://localhost:8000/api/v1/students
```

---
