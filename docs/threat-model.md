# Threat Model

## Project

Secure-by-Design Notes API

## Purpose of This Threat Model

This threat model identifies what needs to be protected, who may interact with the system, what could go wrong, and what security controls will help reduce risk.

The goal is to think about security before writing code instead of trying to add security later.

## Assets

Assets are the important things this API must protect.

The main assets are:

* User notes
* User account information
* Password hashes
* Authentication tokens
* User roles
* Audit logs
* Environment variables and secrets
* Database records

## Actors

Actors are the people or systems that interact with the API.

### Unauthenticated User

An unauthenticated user is someone who is not logged in. This person should only be able to register or log in. They should not be able to view, create, edit, or delete notes.

### Authenticated User

An authenticated user is someone who has registered and logged in. This user should be able to create, read, update, and delete only their own notes.

### Administrator

An administrator is a trusted user with extra permissions. Admin-only actions should be protected with role-based access control.

### Attacker

An attacker is someone who tries to misuse the API. The attacker may be logged in or not logged in. They may try to steal notes, guess passwords, bypass login, access another user's data, become an admin, or break the application.

## Trust Boundaries

A trust boundary is a place where data moves from one area to another and should not automatically be trusted.

The main trust boundaries are:

1. Client to API
2. API to Database
3. API to External Tools or Dependencies

### Client to API

The API should not automatically trust anything sent by the client. The client could send invalid data, missing tokens, fake tokens, harmful input, or requests for resources they do not own.

### API to Database

The API must safely communicate with the database. It should avoid unsafe queries, protect stored data, and make sure users can only access records they are allowed to see.

### API to Dependencies

The API relies on third-party Python packages. These packages may contain security weaknesses, so they should be locked to specific versions, scanned, and updated regularly.

## Common Attacker Goals

An attacker may try to:

* View another user's notes
* Edit or delete another user's notes
* Create an account using harmful input
* Guess passwords
* Use a fake or expired token
* Become an admin without permission
* Insert malicious input
* Cause errors that reveal system details
* Abuse the API by sending too many requests
* Exploit vulnerable dependencies

## Misuse Cases

### Misuse Case 1: Accessing Another User's Note

A logged-in user changes the note ID in a request to try to view another user's note.

**Security Control:**

The API must verify note ownership before returning, updating, or deleting a note.

### Misuse Case 2: Missing Authentication

A user tries to access notes without logging in.

**Security Control:**

Protected routes must require a valid authentication token.

### Misuse Case 3: Broken Role Checks

A regular user tries to access an admin-only route.

**Security Control:**

Admin routes must verify the user's role before allowing access.

### Misuse Case 4: Injection Attempt

A user submits suspicious input that looks like SQL commands or code.

**Security Control:**

The API must validate input and use safe database queries through the ORM.

### Misuse Case 5: Password Attack

An attacker tries many passwords in a short period of time.

**Security Control:**

The API should use password hashing, safe error messages, and rate limiting.

### Misuse Case 6: Token Abuse

An attacker tries to use an invalid, fake, expired, or modified token.

**Security Control:**

The API must verify tokens before allowing access.

### Misuse Case 7: Dependency Vulnerability

A Python package used by the project has a known security weakness.

**Security Control:**

The project should use dependency scanning tools such as pip-audit and Dependabot.

## Security Decisions

This API will use authentication to protect note routes. It will use authorization checks to make sure users can only access their own notes. Passwords will be hashed instead of stored as plain text. User input will be checked before processing. Sensitive settings will be stored in environment variables. The project will include tests for both normal use and misuse cases. Security scanning will run during development.
