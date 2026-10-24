# Job Application Tracker API

A Python REST API for tracking job applications, built with FastAPI and SQLite. This project demonstrates CRUD operations, input validation, duplicate detection, and automated API integration testing.

## Features

- Create and list job applications
- Update application statuses
- Delete applications
- Validate company names and job titles
- Detect duplicates regardless of capitalization or surrounding whitespace
- Return meaningful HTTP error responses
- Test API behavior with an isolated temporary SQLite database

## Tech Stack

- Python
- FastAPI
- SQLite
- Uvicorn
- unittest
- FastAPI TestClient / HTTPX

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd remote-journey
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Git Bash on Windows:

```bash
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the API

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint             | Description                    |
| ------ | -------------------- | ------------------------------ |
| GET    | `/applications`      | List applications              |
| POST   | `/applications`      | Create an application          |
| PATCH  | `/applications/{id}` | Update an application's status |
| DELETE | `/applications/{id}` | Delete an application          |

### Create an application

```json
{
  "company": "Example Company",
  "position": "Backend Engineer"
}
```

New applications receive the default status `Applied`.

### Update a status

```json
{
  "status": "Interview"
}
```

Allowed statuses: `Applied`, `Interview`, `Rejected`, and `Accepted`.

## Run Tests

Run the API integration tests:

```bash
python -m unittest test_api.py -v
```

Run the database tests:

```bash
python -m unittest test_database.py -v
```

Run all tests:

```bash
python -m unittest discover -v
```

## Project Structure

```text
remote-journey/
├── database.py
├── main.py
├── test_api.py
├── test_database.py
├── requirements.txt
├── README.md
├── .gitignore
└── .github/
    └── workflows/
        └── tests.yml
```

## Future Improvements

- Database-level duplicate constraints
- Stronger request schemas and validation
- Pagination and filtering
- Authentication and authorization
- PostgreSQL support
- Frontend integration
- Continuous integration with GitHub Actions

## Learning Goals

This project is part of a practical journey toward backend and full-stack engineering roles, with an emphasis on maintainable code, API design, persistence, testing, and deployment.
