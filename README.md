# Backend Development Report: Blog API

## Project Overview


This report details the implementation of a comprehensive backend development task focused on creating a RESTful API for a blog application. The API handles CRUD operations for posts, comments, and users, incorporating various aspects such as database design, API creation, authentication, and deployment. Additionally, the project integrates Celery and Redis for asynchronous email functionality. The following sections outline the completed work, addressing each requirement and providing insights into the implementation process.

  

## Objectives

  

The primary objectives of this project were to:

  

1. Create a RESTful API for a simple blog application.

2. Implement user authentication and authorization.

3. Integrate asynchronous email functionality using Celery and Redis.

4. Ensure the application is ready for deployment.

  

## Requirements and Implementation

  

### User Stories

  

1.  **User Registration and Login:**

- Implemented endpoints for user registration and login.

- Utilized Django's authentication system and JWT for secure user authentication.

- Integrated Celery and Redis to send registration and login notification emails asynchronously.

2.  **CRUD Operations for Posts and Comments:**

- Developed endpoints for creating, reading, updating, and deleting posts and comments.

- Implemented permissions to ensure only authenticated users can create and manage their own posts and comments.

3.  **Viewing Posts and Comments:**

- Created endpoints to allow users to view posts and comments created by other users.

  

### Entities and Database Design

  

The database schema was designed based on the specified entities:

  

-  **User**: `id`, `username`, `email`, `password`

-  **Post**: `id`, `title`, `content`, `authorId`, `createdAt`, `updatedAt`

-  **Comment**: `id`, `postId`, `authorId`, `content`, `createdAt`, `updatedAt`

  

The schema was normalized to ensure efficient data storage and retrieval. The MySQL relational database was used, with Django's ORM handling the database interactions.

  

### API Endpoints

  

The API endpoints were developed as follows:

  

#### User Endpoints

  

-  `POST /api/users/register` - Register a new user

-  `POST /api/users/login` - Authenticate user and return a token

-  `GET /api/users/profile` - Get user profile (Authenticated)

  

#### Post Endpoints

  

-  `GET /api/posts` - Retrieve all posts (Paginated)

-  `GET /api/posts/:id` - Retrieve a single post by ID

-  `POST /api/posts` - Create a new post (Authenticated)

-  `PUT /api/posts/:id` - Update a post by ID (Authenticated & Author only)

-  `DELETE /api/posts/:id` - Delete a post by ID (Authenticated & Author only)

  

#### Comment Endpoints

  

-  `GET /api/posts/:postId/comments` - Retrieve all comments for a post (Paginated)

-  `POST /api/posts/:postId/comments` - Create a new comment on a post (Authenticated)

-  `PUT /api/comments/:id` - Update a comment by ID (Authenticated & Author only)

-  `DELETE /api/comments/:id` - Delete a comment by ID (Authenticated & Author only)

  

### Celery and Redis Integration

  

- Implemented **Celery** for background task processing and **Redis** as the message broker.

- Used Celery to send registration and login notification emails asynchronously:

- On user registration, a welcome email is sent.

- On login, a notification email is sent with details like IP address, device type, and login time.

- Improved performance by offloading email-sending tasks from the main API flow to Celery workers.

  

#### Email Functionality

  

-  **Welcome Email**: Sent after successful user registration to welcome new users.

-  **Login Notification Email**: Sent after user login, including details such as IP address, device type, and login time for security purposes.

  

#### Benefits of Using Celery and Redis:

  

- Reduced response times for user registration and login requests.

- Scalability to handle a high volume of emails.

- Reliability through Redis as a fault-tolerant message broker.

  
  

### Authentication & Authorization

  

- Implemented JWT for user authentication to secure the endpoints.

- Protected routes that require authentication, ensuring only authorized users can access certain operations.

- Implemented role-based access to ensure users can only update or delete their own posts and comments.

  

### Pagination and Search Functionality

  

- Implemented pagination for listing posts and comments.

- Added search functionality to allow users to find posts based on keywords.

  

### Continuous Integration and Continuous Deployment (CI/CD)

  

- Set up a CI/CD pipeline using GitHub Actions for automated testing and deployment.

- Configured the pipeline to run tests on every push to the repository, ensuring code quality and functionality.

- Deployed the application using Docker for containerization, with a `Dockerfile` and `docker-compose.yml` provided for easy setup.

  

### Deployment

  

- Dockerized the application for easy deployment.

- Prepared the application for deployment on Digital Ocean Droplet.

- Included necessary configurations for environment variables and database connections.

  

## Testing

  

- Implemented unit and integration tests for critical parts of the application using Django's testing framework.

- Ensured tests cover user registration, authentication, CRUD operations for posts and comments, and permissions.

- Automated tests were integrated into the CI/CD pipeline to ensure reliability and prevent regressions.

  

## Setup

### Prerequisites

- Docker

- Docker Compose

  

### Running the application

1. Clone the repository:

```sh

git  clone  https://github.com/samuelogboye/blogapi.git

cd  blogapi

```

2. Create a `.env` file based on `.env.example` and update your database credentials.

  

3. Build and start the containers:

```sh

docker  compose  up  --build

```

6. Access the API at `http://localhost:8000/api/docs`

  

### Running Tests

Run the tests with:

```sh

docker  compose  exec  web  python  manage.py  test

```

### API Documentation

Postman collection for API documentation and sample requests.

- [Blog API Postman Collection](https://documenter.getpostman.com/view/28919661/2sA3kYk1S3)

- [Swagger Documentation](http://64.23.128.5:8000/api/docs)

  

## Deployment

The application is ready to be deployed on a cloud provider

  

## Submission

  

The project has been committed to a GitHub repository. The repository includes:

  
- Complete source code.

- Instructions for setting up and running the application in the `README.md` file.

- Sample data and API documentation (e.g., Postman collection).


## Conclusion

This report outlines the successful implementation of a comprehensive backend development task. The project demonstrates proficiency in database design, API creation, authentication, authorization, deployment, and asynchronous task handling using Celery and Redis. The application is well-prepared for deployment and provides a robust foundation for further development and enhancements.