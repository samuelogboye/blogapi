# Blog API

This is a simple blog API built with Django. It handles CRUD operations for posts, comments, and users, with JWT authentication.

## Features

- User registration and login
- CRUD operations for posts and comments
- JWT authentication
- Dockerized for easy setup and deployment

## Setup

### Prerequisites

- Docker
- Docker Compose

### Running the application

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd blogapi
    ```

2. Create a `.env` file based on `.env.example` and update your database credentials.

3. Build and start the containers:
    ```sh
    docker-compose up -d
    ```

4. Apply migrations:
    ```sh
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

6. Access the API at `http://localhost:8000`.

### Running Tests

Run the tests with:
```sh
docker-compose exec web python manage.py test
