### Address Book API (FastAPI & SQLite)

## Table of Contents:
1. Overview
2. Features
3. Tech Stack
4. Project Structure
5. Setup and Installation
6. Prerequisites
    Option 1: Using Docker Compose (Recommended)
    Option 2: Local Setup with Poetry
7. Running the Application
8. API Endpoints
9. Testing
10. Design Decisions & Best Practices
11. Future Enhancements
12. Author

--------------------------------------------------------------------------------------------------

## 1. Overview

This project implements a minimal Address Book API built with FastAPI. It allows users to manage addresses, including creating, retrieving, updating, and deleting records. A key feature is the ability to query for addresses located within a specified geographic distance from a given point. The application uses an SQLite database for storage and is designed with clean architecture principles, automated testing, and Docker containerization for easy deployment.

## 2. Features

* Address Management (CRUD):
POST /api/v1/addresses/: Create a new address with name, latitude, and longitude.
GET /api/v1/addresses/{address_id}: Retrieve a single address by its unique ID.
PUT /api/v1/addresses/{address_id}: Update an existing address.
DELETE /api/v1/addresses/{address_id}: Delete an address record.

* Geospatial Query:
GET /api/v1/addresses/nearby: Retrieve all addresses within a specified radius_km from a given latitude and longitude.

* Data Validation:
All incoming address data (latitude and longitude ranges) is validated using Pydantic.

* SQLite Database:
Persistent storage for address records.

* Interactive API Documentation:
Automatically generated Swagger UI and ReDoc by FastAPI.

* Robust Logging:
Structured logging for application events and requests.

* Automated Testing:
Comprehensive unit and integration tests using pytest.

* Containerization:
Dockerfile and Docker Compose setup for reproducible environments and easy deployment.

## 3. Tech Stack

Python 3.12+: The core programming language.
FastAPI: High-performance web framework for building APIs.
Pydantic: Data validation and settings management (integrated with FastAPI).
SQLAlchemy: Python SQL toolkit and Object-Relational Mapper (ORM) for database interactions.
Alembic: Lightweight database migration tool for SQLAlchemy.
GeoPy: Library for geodesic distance calculations (used for the "nearby" feature).
Poetry: Dependency management and packaging.
Pytest: Testing framework.
HTTPX: Asynchronous HTTP client for API testing.
Uvicorn: ASGI server to run the FastAPI application.
Ruff: An extremely fast Python linter and formatter.
Docker / Docker Compose: For containerization and easy local deployment.

## 4. Project Structure

The project follows a modular and layered architecture to separate concerns, making it maintainable and scalable.

address-book-api/
├── .dockerignore                 # Specifies files/folders to exclude from Docker image
├── .env                          # Environment variables (local dev, ignored by Git)
├── .gitignore                    # Files/folders ignored by Git
├── alembic/                      # Alembic migrations directory
│   ├── versions/                 # Migration scripts live here
│   └── env.py                    # Alembic environment configuration
├── Dockerfile                    # Instructions for building the Docker image
├── docker-compose.yml            # Defines how to run services with Docker
├── poetry.lock                   # Locks dependency versions
├── pyproject.toml                # Project metadata and dependency definitions (Poetry)
├── README.md                     # This file!
├── app/                          # Main application source code
│   ├── __init__.py               # Makes 'app' a Python package
│   ├── main.py                   # FastAPI application instance, entry point
│   ├── api/                      # API-related logic
│   │   ├── __init__.py
│   │   ├── dependencies.py       # FastAPI dependency for database session
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       └── endpoints/        # API endpoints/routes
│   │           ├── __init__.py
│   │           └── addresses.py  # Address CRUD and geospatial endpoints
│   ├── core/                     # Core application configuration and utilities
│   │   ├── __init__.py
│   │   ├── config.py             # Pydantic-based settings management
│   │   └── logging_config.py     # Centralized logging configuration
│   ├── crud/                     # Create, Read, Update, Delete (CRUD) operations for database
│   │   ├── __init__.py
│   │   └── crud_address.py       # CRUD functions for Address model
│   ├── db/                       # Database session and base setup
│   │   ├── __init__.py
│   │   └── session.py            # SQLAlchemy engine and session creation
│   ├── models/                   # SQLAlchemy ORM models (database table definitions)
│   │   ├── __init__.py
│   │   └── address.py            # SQLAlchemy model for Address
│   └── schemas/                  # Pydantic schemas (for request/response validation/serialization)
│       ├── __init__.py
│       └── address.py            # Pydantic schemas for Address data (create, read, update)
└── tests/                        # Automated tests
    ├── __init__.py
    ├── conftest.py               # Pytest fixtures for test setup (e.g., test database)
    └── test_api/                 # Tests for API endpoints
        ├── __init__.py
        └── test_addresses.py     # Tests for Address CRUD and geospatial features

## 5. Setup and Installation

* Prerequisites

Ensure you have the following installed on your system:
Git: For cloning the repository.
Python 3.12+: For local development (check python3 --version).
Poetry: Python dependency manager (install with pip install poetry).
Docker Desktop: For running the application using containers.

# Option 1: Using Docker Compose (Recommended)

This is the easiest and most reliable way to get the application running, as it sets up all dependencies and the environment automatically.

* 1. Clone the repository:
```python
git clone https://github.com/your-username/address-book-api.git
cd address-book-api
```

* 2. Build the Docker image:
```python
docker-compose build
```

* 3. Start the services: This will create the db_data volume, run Alembic migrations to create the address_book.db file and addresses table inside the volume, and start the FastAPI application.
``` python
docker-compose up
# Or to run in detached mode (in the background):
# docker-compose up -d
```

* 4. The API will be available at http://localhost:8000. The interactive documentation (Swagger UI) is at http://localhost:8000/docs.

To stop the services:

```python
docker-compose down
# To stop and remove the persistent database volume (for a clean slate):
# docker-compose down -v
```

# Option 2: Local Setup with Poetry

* 1. Clone the repository:
```python
git clone https://github.com/your-username/address-book-api.git
cd address-book-api
```
* 2. Install dependencies using Poetry: This will create a virtual environment and install all required libraries.

```python
poetry install
```

* 3. Activate the virtual environment (if not already active by your IDE):

```python
poetry shell
```

* 4. Run database migrations: This will create the address_book.db SQLite file in your project root and set up the addresses table.
```python
poetry run alembic upgrade head
```

* 5. (Optional) Create a .env file: Create a file named .env in the project root to override default settings (e.g., DATABASE_URL=sqlite:///./my_custom_address_book.db).

## 6. Running the Application

Once set up (either Docker or locally), run the FastAPI application:

* With Docker Compose (if already up):
    The application will be running from docker-compose up.

* Locally with Poetry:
```python
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
(The --reload flag is great for development as it restarts the server on code changes.)

The API will be accessible at http://localhost:8000.
The interactive API documentation (Swagger UI) can be found at: http://localhost:8000/docs.
The alternative documentation (ReDoc) can be found at: http://localhost:8000/redoc.

## 7. API Endpoints

All endpoints are prefixed with `/api/v1/addresses`. You can interact with these endpoints via the [Swagger UI](http://localhost:8000/docs) after running the application.

| Method | Path | Description | Request Body | Query Parameters | Response |
| :------: | :-------------------------- | :------------------------------------------------------------------------ | :------------------------------------------------------ | :------------------------------------------- | :-------------------- |
| `POST` | `/`                         | Creates a new address record.                                             | `name: str`, `latitude: float`, `longitude: float`      | -                                            | `Address` (with `id`) |
| `GET`  | `/{address_id}`             | Retrieves a single address by its unique ID.                              | -                                                       | -                                            | `Address`             |
| `PUT`  | `/{address_id}`             | Updates an existing address.                                              | `name: str`, `latitude: float`, `longitude: float`      | -                                            | `Address`             |
| `DELETE` | `/{address_id}`           | Deletes an address by ID.                                                 | -                                                       | -                                            | `Address`             |
| `GET`  | `/nearby`                   | Retrieves addresses within a specified radius from a given location.      | -                                                       | `latitude: float`, `longitude: float`, `radius_km: float` | `List[Address]`       |

## 8. Testing

Automated tests are included to ensure the correctness and robustness of the API.

* 1. Ensure you are in the project root directory.
* 2. Run tests using Poetry:
```python
poetry run pytest
```
This will execute all tests defined in the tests/ directory. Fixtures in tests/conftest.py ensure that tests run against an isolated, in-memory SQLite database that is cleaned up after each test, guaranteeing repeatability.

## 9. Design Decisions & Best Practices

This project adheres to several best practices for building robust and maintainable APIs:

* FastAPI Framework: Chosen for its high performance, native asynchronous support, automatic interactive API documentation (Swagger UI/ReDoc), and strong type hints powered by Pydantic.

* Clear Project Structure: Logical separation of concerns into api, crud, models, schemas, core, and db layers. This enhances readability, maintainability, and testability.

* Pydantic for Data Validation & Serialization: Used extensively for:
    - Input Validation: Ensures incoming request bodies conform to expected schemas and rules (e.g., latitude/longitude ranges), returning clear 422 Unprocessable Entity errors automatically.
    - Output Serialization: Ensures API responses are consistently formatted and only contain intended fields (response_model).

* SQLAlchemy ORM with Alembic Migrations:
    - SQLAlchemy: Provides a powerful, Pythonic way to interact with the database, abstracting away raw SQL.
    - Alembic: Manages database schema changes in a controlled and versioned manner, essential for evolving applications.

* Dependency Injection: FastAPI's Depends system is used for managing database sessions (get_db). This makes endpoint functions clean, testable, and ensures sessions are properly opened and closed for each request.

* Comprehensive Testing with pytest:
    - TestClient: Allows making requests directly to the FastAPI app in tests without a running server.
    - conftest.py Fixtures: Sets up an ephemeral, in-memory SQLite database for each test run, with transactional rollbacks, ensuring each test is completely isolated and repeatable.

* Configuration Management (pydantic-settings): Application settings (like DATABASE_URL, ENVIRONMENT) are managed via app/core/config.py and can be easily overridden by environment variables or a .env file, facilitating deployment across different environments.

* Structured Logging (logging.dictConfig): Configured to provide informative output for application events, startup/shutdown, and API requests, aiding in debugging and monitoring. Logs are emitted to stdout, suitable for containerized environments.

* Containerization with Docker:
    - Dockerfile: Defines a clean, multi-stage build process to create a lightweight and efficient Docker image for the application, separating build dependencies from runtime.
    - docker-compose.yml: Orchestrates the application stack, enabling one-command setup, managing network ports, and ensuring database persistence via Docker volumes (db_data). The command ensures migrations run before the app starts.

* Code Quality Tools (Ruff): Used for fast linting and automatic code formatting, ensuring consistent and clean code.

* Geospatial Library (geopy): Leveraged for accurate geodesic distance calculations, rather than reinventing complex mathematical formulas.

## 10. Future Enhancements

* Authentication and Authorization: Implement user authentication (e.g., JWT) and define access controls for API endpoints (e.g., only authenticated users can create addresses, only owner can delete).

* Improved Error Handling: More granular custom exception handling for specific business logic errors.

* Advanced Geospatial Queries:
    - Add spatial indexing to the database for more efficient queries on large datasets.
    - Implement more complex search criteria (e.g., "find addresses in a polygon").

* Pagination for get_all_addresses and get_nearby_addresses: For very large numbers of addresses, returning all of them at once can be inefficient.

* Background Tasks: For potentially long-running operations (though not needed for this assignment).

* Caching: Implement a caching layer for frequently accessed data to improve performance.

## 11. Author

Ajinkya Chikhlodkar
[Your GitHub Profile Link, if you wish]

