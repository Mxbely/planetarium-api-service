# Planetarium API Service

The Planetarium API Service is a Django REST Framework-based application that allows managing planetarium show bookings,
ticket reservations, and viewing information about astronomy shows, available domes, and show themes.

## Key Features

- Manage show themes.
- View, create, update, and delete astronomy shows.
- Manage planetarium domes (seats, halls, etc.).
- Schedule astronomy show sessions.
- Ticket reservation system for shows.
- Authentication using JWT tokens.
- API response caching for improved performance.

## Prerequisites

Make sure you have the following tools installed on your system:

- Docker and Docker Compose
- Python 3.12+
- Redis for caching

## Running the Project with Docker-Compose

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd planetarium-api-service
   ```

2. Create a `.env` file in the root directory of the project:
   ```env
   SECRET_KEY='<your-django-secret-key>'
   ```

3. Start the application using Docker-Compose:
   ```bash
   make docker
   ```
   or
   ```bash
   docker-compose up --build
   ```

4. The API will be available at: [http://localhost:8000](http://localhost:8000).

### Docker-Compose Configuration

- **app**: The Django application.
- **redis**: Caching service for API responses.
- **redisinsight**: A tool for monitoring Redis.

### Database Management

The project uses SQLite as the default database. You can modify the `settings.py` file to switch to PostgreSQL or
another database of your choice.

## User Management

### Creating a Superuser

To access the admin panel:

```bash
make docker-superuser
```

You can then access the admin panel at: [http://localhost:8000/admin](http://localhost:8000/admin).

## API Documentation

The project provides interactive API documentation using `drf-spectacular`:

- Swagger: [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/)
- Redoc: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

## Testing

Unit tests cover the core API logic. To run tests, execute:

```bash
make docker-test
```

## Project Structure

- **planetarium/**
    - API logic for managing planetarium shows, domes, and tickets.
    - Serializers, models, and views.
- **accounts/**
    - Custom user model implementation based on email authentication.

## Key Dependencies

- Django==5.1.4
- Django REST Framework
- Django Filters
- Redis
- drf-spectacular
- JWT (JSON Web Token)

## Future Enhancements

- Add support for other databases (e.g., PostgreSQL).
- Implement background tasks for booking management (e.g., Celery).
- Introduce monitoring and logging for API requests (e.g., via Sentry).
