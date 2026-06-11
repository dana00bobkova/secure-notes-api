# Architecture

## Project Name

Secure-by-Design Notes API

## Project Purpose

The Secure Notes API is a small multi-user API that lets users register, log in, and manage private notes. The goal of this project is to demonstrate secure coding, authentication, authorization, input validation, audit logging, automated testing, and DevSecOps security scanning.

This project is intentionally small. Instead of building a large application with many features, the focus is on creating a simple API with strong security protections.

## Domain

The project focuses on private user notes.

Users can create notes such as reminders, study notes, personal notes, or task lists. Each note belongs to one specific user. Users should only be able to view, edit, or delete their own notes.

For example, if Dana and Bob both have accounts, Dana should not be able to see Bob's notes, and Bob should not be able to edit Dana's notes.

## Main Features

The API supports basic account management and note management.

### Account Management

* Register a new user account
* Log in
* Receive an authentication token
* Use the token to access protected routes
* Support user roles such as regular user and admin

### Note Management

The API supports CRUD operations:

* Create a note
* Read notes
* Update a note
* Delete a note

CRUD stands for Create, Read, Update, and Delete. These are the basic actions most applications perform on stored data.

## Main Components

The system has three main parts:

1. Client
2. API
3. Database

The client is the person or tool sending requests. This could be a web browser, Postman, curl, or a future frontend application.

The API is the FastAPI application. It receives requests, checks whether the user is logged in, validates input, checks permissions, performs the requested action, and returns a response.

The database stores users, password hashes, notes, roles, and audit log records.

## Basic Data Flow

The basic data flow is:

Client → API → Database

A user sends a request to the API. The API reviews the request and communicates with the database when needed. The database returns information to the API, and the API sends a response back to the user.

## Security Goals

The main security goals are:

* Users must log in before accessing private notes.
* Users can only access their own notes.
* Admin-only actions must be limited to admin users.
* Passwords must be hashed and never stored as plain text.
* User input must be checked before processing.
* Sensitive settings must be stored in environment variables instead of hardcoded values.
* Security-related events should be logged.
* Automated tests and security scans should run before code is merged.

## Out of Scope

The first version of this project will not include a large frontend, payment processing, file uploads, messaging, email verification, or advanced cloud deployment.

These features are intentionally excluded so the project can focus on secure API design and DevSecOps practices.
