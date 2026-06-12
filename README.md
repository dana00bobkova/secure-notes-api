# Secure-by-Design Notes API

![CI Security Checks](https://github.com/dana00bobkova/secure-notes-api/actions/workflows/ci.yml/badge.svg)
![CodeQL Security Scan](https://github.com/dana00bobkova/secure-notes-api/actions/workflows/codeql.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Secure%20API-green)
![Security](https://img.shields.io/badge/Security-DevSecOps%20Project-purple)

## Project Overview

Secure-by-Design Notes API is a small multi-user API built with FastAPI. It allows users to register, log in, and manage private notes. The main goal of this project is to demonstrate secure coding, authentication, authorization, input validation, audit logging, automated testing, and DevSecOps security scanning.

This project is intentionally small so the focus stays on building a simple API with strong security protections.

## Project Purpose

The purpose of this project is to show how a basic web API can be designed with security in mind from the beginning. Instead of adding security at the end, this project includes authentication, note ownership checks, validation, audit logging, tests, and automated security checks as part of the development process.

## Main Features

* User registration
* User login with JWT tokens
* Protected routes
* Private user notes
* Create, read, update, and delete notes
* Note ownership checks
* Role field support for future admin features
* Input validation with Pydantic
* Password hashing with bcrypt
* Audit logging for important security events
* Automated tests with Pytest
* Test coverage reporting
* GitHub Actions CI pipeline
* Bandit Python security scanning
* pip-audit dependency vulnerability scanning
* CodeQL code scanning
* Dependabot dependency update monitoring

## Security Features

### Authentication

Users must register and log in before accessing protected routes. Login returns a JWT access token, which is required for private note operations.

### Authorization

Each note belongs to one user. Users can only view, update, or delete their own notes. If a user tries to access another user's note, the API returns a generic `404 Not Found` response.

### Password Security

Passwords are never stored in plain text. User passwords are hashed before being saved to the database.

### Input Validation

The API validates user input for account registration, login, and note creation. Invalid emails, short passwords, empty note titles, and empty note content are rejected.

### Audit Logging

The API records important security events, including:

* User registration
* Failed registration attempts
* Successful login
* Failed login attempts
* Note creation
* Note updates
* Note deletion
* Unauthorized or missing note access attempts

Audit logs include event type, user ID when available, email, success status, IP address, safe event details, and timestamp. Passwords, tokens, and private note contents are not stored in audit logs.

## DevSecOps Pipeline

This project includes a GitHub Actions CI pipeline that automatically runs on pushes and pull requests.

The pipeline runs:

* Pytest automated tests
* Test coverage reporting
* Bandit security scan
* pip-audit dependency scan

The project also includes CodeQL code scanning and Dependabot dependency monitoring.

## Testing

The test suite checks both normal behavior and security misuse cases.

Tests include:

* User registration
* Login success
* Login failure
* Duplicate email rejection
* Invalid email rejection
* Short password rejection
* Protected notes route enforcement
* Note creation
* Note listing
* Note reading
* Note updating
* Note deletion
* User cannot read another user's note
* User cannot update another user's note
* User cannot delete another user's note
* Audit log creation for important events

To run tests locally:

```bash
pytest -v
```

To run coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Security Scanning

Run Bandit locally:

```bash
bandit -r app
```

Run pip-audit locally:

```bash
pip-audit -r requirements.txt
```

## Tech Stack

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* JWT authentication
* Pytest
* GitHub Actions
* Bandit
* pip-audit
* CodeQL
* Dependabot

## API Endpoints

### Authentication

| Method | Endpoint         | Description                         |
| ------ | ---------------- | ----------------------------------- |
| POST   | `/auth/register` | Register a new user                 |
| POST   | `/auth/login`    | Log in and receive a JWT token      |
| GET    | `/auth/me`       | View the current authenticated user |

### Notes

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| POST   | `/notes/`          | Create a note             |
| GET    | `/notes/`          | List current user's notes |
| GET    | `/notes/{note_id}` | Read one note             |
| PUT    | `/notes/{note_id}` | Update one note           |
| DELETE | `/notes/{note_id}` | Delete one note           |

### Health

| Method | Endpoint  | Description           |
| ------ | --------- | --------------------- |
| GET    | `/health` | Health check endpoint |

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./secure_notes.db
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## OWASP Mapping

| OWASP Risk                               | Project Control                                         |
| ---------------------------------------- | ------------------------------------------------------- |
| Broken Access Control                    | Note ownership checks and protected routes              |
| Cryptographic Failures                   | Password hashing and environment-based secret handling  |
| Injection                                | Input validation and ORM queries                        |
| Insecure Design                          | Misuse-case testing and secure architecture decisions   |
| Authentication Failures                  | JWT validation and password verification                |
| Software and Data Integrity Failures     | CI pipeline, dependency scanning, and Dependabot        |
| Security Logging and Monitoring Failures | Audit logging for important security events             |
| Security Misconfiguration                | `.env`, `.env.example`, and safe configuration handling |

## Project Status

This project is a portfolio security engineering project. It demonstrates secure API development, automated testing, audit logging, and DevSecOps practices in a small but complete application.

## Evidence Screenshots

This project includes evidence screenshots showing that the API, tests, coverage, audit logging, and DevSecOps pipeline are working.

| Evidence | Screenshot |
|---|---|
| Swagger UI API documentation | `docs/evidence/swagger-ui.png` |
| Local Pytest results | `docs/evidence/tests-passed.png` |
| Test coverage report | `docs/evidence/coverage-report.png` |
| GitHub Actions passing run | `docs/evidence/github-actions-green.png` |
| CodeQL code scanning | `docs/evidence/codeql-scan.png` |
| Dependabot monitoring | `docs/evidence/dependabot.png` |
| Audit log database output | `docs/evidence/audit-logs.png` |