# Task Manager Backend
This repository contains the backend service for a Task Manager application, built with Django and Django REST Framework (DRF). It provides a RESTful API to manage tasks, supporting full CRUD functionality along with advanced features like filtering, sorting, and pagination. The entire application is containerized with Docker for a streamlined development and deployment experience.
## DockerHub
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-task--manager-blue)](https://hub.docker.com/r/akramaliii/task-manager)

## Technologies
 ### Backend Framework: Django, Django REST Framework (DRF)

### Database: PostgreSQL

### Containerization: Docker, Docker Compose

## Setup and Run Instructions
The easiest way to get the backend running is by using Docker Compose, which will automatically build the application image and spin up a PostgreSQL database container.

 ## 1. Clone the Repository
Start by cloning the project from GitHub and navigating into the directory.
``` bash
git clone https://github.com/akram3855/task_manger_backend.git
cd task_manger_backend
```

## 2. Configure Environment Variables
Create a .env file in the root directory and copy the contents from the provided .env.example file. Be sure to replace the placeholder values with a strong SECRET_KEY and your desired API_KEY.
```bash
cp .env.example .env
```

 ## 3. Run the Application

Use Docker Compose to build and start the containers in detached mode (-d). This command will also install all required Python packages.
```bash
docker-compose up --build -d
```

## 4. Apply Database Migrations
Once the containers are running, you need to apply the database migrations to set up the necessary tables in your PostgreSQL database.
```bash
docker-compose exec web python manage.py migrate
```

The backend API will now be live and accessible at http://localhost:8000.

## API Usage Examples
The API is accessible at http://localhost:8000/api/tasks/. All endpoints require authentication via a custom API key provided in the Authorization header.

Replace `[YOUR_API_KEY]` with the key you set in your .env file.

## 1. Create a Task (POST)
To create a new task, send a POST request with the required fields in a JSON body.
```bash
curl -X POST http://localhost:8000/tasks/ \
-H "Content-Type: application/json" \
-H "Authorization: Api-Key 12345678" \
-d '{
  "title": "Build a CI/CD pipeline",
  "description": "Automate the testing and deployment workflow.",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2025-09-15T10:00:00Z"
}'
```

## 2. List Tasks (GET)
Retrieve a paginated list of tasks with support for filtering and sorting.
```bash
# Get all tasks with default pagination
curl -X GET http://localhost:8000/api/tasks/ \
-H "Authorization: Api-Key [YOUR_API_KEY]"


# Filter by status and priority

curl -X GET "http://localhost:8000/api/tasks/?status=done&priority=low" \
-H "Authorization: Api-Key [YOUR_API_KEY]"

# Search for "docker" in titles and descriptions
curl -X GET "http://localhost:8000/api/tasks/?search=docker" \
-H "Authorization: Api-Key [YOUR_API_KEY]"

# Sort by due date in descending order
curl -X GET "http://localhost:8000/api/tasks/?ordering=-due_date" \
-H "Authorization: Api-Key [YOUR_API_KEY]"
```

## 3. Retrieve a Single Task (GET)
Fetch the details of a specific task using its unique id.
```bash

curl -X GET http://localhost:8000/api/tasks/[TASK_ID]/ \
-H "Authorization: Api-Key [YOUR_API_KEY]"
```
## 4. Update a Task (PATCH)
Update one or more fields of an existing task. Use PATCH for a partial update.
```bash
curl -X PATCH http://localhost:8000/api/tasks/[TASK_ID]/ \
-H "Content-Type: application/json" \
-H "Authorization: Api-Key [YOUR_API_KEY]" \
-d '{"status": "done"}'
```
## 5. Delete a Task (DELETE)
Permanently delete a task using its unique id.
```bash
curl -X DELETE http://localhost:8000/api/tasks/[TASK_ID]/ \
-H "Authorization: Api-Key [YOUR_API_KEY]"

```

## Assumptions and Limitations
Development Environment: The provided Docker setup is optimized for local development. For a production environment, you would need a more robust setup, including a production-ready web server like Gunicorn and a more secure configuration.

Database: The application is configured to use PostgreSQL. While the Docker Compose setup manages this, the code itself assumes a PostgreSQL backend.

Authentication: The current API key authentication is a simple, stateless approach suitable for this assessment. In a real-world application, a more robust authentication mechanism like token-based or OAuth would be preferred.
