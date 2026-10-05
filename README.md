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

# Milestone 4 — CI Pipeline with GitHub Actions

The fourth milestone focuses on implementing a CI pipeline using GitHub Actions and a self-hosted GitHub Actions runner.

The pipeline automatically validates the application, runs tests and linting, builds the Docker image, and publishes the image to Docker Hub.

## What Was Implemented

- GitHub Actions CI workflow
- Self-hosted GitHub Actions runner
- API build stage
- Automated unit testing
- Automated code linting using Ruff
- Docker Buildx
- Secure Docker Hub authentication using GitHub Secrets
- Docker image build and push
- Path-based CI triggering
- Manual workflow triggering
- Versioned Docker image publishing

---

## CI Pipeline Flow

```text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Checkout Code
    │
    ├── Build API
    │
    ├── Run Tests
    │
    ├── Run Lint
    │
    ├── Setup Docker Buildx
    │
    ├── Login to Docker Hub
    │
    ├── Build Docker Image
    │
    └── Push Docker Image
              │
              ▼
          Docker Hub
```

---

## GitHub Actions Workflow

The CI workflow is defined in:

```text
.github/workflows/ci.yml
```

The pipeline runs on a self-hosted GitHub Actions runner:

```yaml
runs-on: self-hosted
```

---

## Pipeline Stages

### 1. Checkout Code

The workflow checks out the repository source code using:

```yaml
- name: Checkout Code
  uses: actions/checkout@v4
```

---

### 2. Build API

The API build stage uses the Makefile:

```bash
make build
```

This installs the application dependencies required for testing and validation.

---

### 3. Run Tests

Unit tests are executed using:

```bash
make test
```

The test target runs the Python unit test suite:

```bash
python3 -m unittest discover -s app -p "test_*.py"
```

---

### 4. Run Lint

Ruff is used for Python code linting:

```bash
make lint
```

The linting stage validates the application source code before the Docker image is built.

---

### 5. Setup Docker Buildx

Docker Buildx is configured using:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
```

Buildx provides the Docker build functionality used by the CI pipeline.

---

### 6. Docker Hub Authentication

Docker Hub credentials are stored securely as GitHub repository secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

The credentials are never hardcoded in the workflow.

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

---

### 7. Build and Push Docker Image

The Docker image is built and pushed using:

```yaml
- name: Build and Push Image
  uses: docker/build-push-action@v6
  with:
    context: .
    file: app/Dockerfile
    push: true
    tags: Sandeepkulkarni77/opsfusion-api:1.0.0
```

The image is published to Docker Hub using a semantic version tag:

```text
Sandeepkulkarni77/opsfusion-api:1.0.0
```

---

## CI Trigger Conditions

The pipeline automatically runs when changes are pushed to the `main` branch and the changes are inside the application directory:

```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'app/**'
```

This prevents unrelated changes outside the application directory from automatically triggering CI.

The workflow also supports manual execution:

```yaml
workflow_dispatch:
```

This allows the developer to manually trigger the CI pipeline from GitHub Actions whenever required.

---

## Self-Hosted GitHub Actions Runner

The CI pipeline runs on a self-hosted GitHub Actions runner configured on an Ubuntu machine.

```text
Runner Type : Self-hosted
Operating System : Ubuntu
Architecture : x64
```

The runner is registered with the GitHub repository and executes the CI workflow locally instead of using GitHub-hosted infrastructure.

---

## CI Pipeline Result

The complete CI pipeline successfully completed all required stages:

```text
┌─────────────────────────────┬──────────┐
│ CI Stage                    │ Status   │
├─────────────────────────────┼──────────┤
│ Checkout Code               │ ✔ PASSED │
│ Build API                   │ ✔ PASSED │
│ Run Tests                   │ ✔ PASSED │
│ Run Lint                    │ ✔ PASSED │
│ Setup Docker Buildx         │ ✔ PASSED │
│ Docker Login                │ ✔ PASSED │
│ Docker Build                │ ✔ PASSED │
│ Docker Push                 │ ✔ PASSED │
└─────────────────────────────┴──────────┘
```
## CI Pipeline Execution 

<img width="1528" height="817" alt="image" src="https://github.com/user-attachments/assets/a627d32b-6ed7-41b4-863e-4fdf610cd42f" />

---

## Milestone 4 Outcome

**Milestone 4 is complete.**

The project now has an automated CI pipeline that:

```text
Code Change
    ↓
GitHub Actions
    ↓
Build
    ↓
Test
    ↓
Lint
    ↓
Docker Build
    ↓
Docker Hub
```

The pipeline runs on a self-hosted GitHub Actions runner and securely publishes the versioned Docker image to Docker Hub.
