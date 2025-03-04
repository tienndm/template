# 🐾 Pokémon API Template

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-green.svg)](https://fastapi.tiangolo.com/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-brightgreen.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

A robust implementation of a Pokémon API built with FastAPI, leveraging Clean Architecture principles for a maintainable and scalable codebase.

## 📑 Table of Contents

- [Description](#-description)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Development](#-development)
- [License](#-license)

## 📝 Description

This project demonstrates Clean Architecture in a Python FastAPI application with the following principles:

1. **Framework Independence**: System operates independently of external libraries or frameworks
2. **Testability**: Business rules can be validated without external elements
3. **UI Independence**: User interface changes don't affect the underlying system
4. **Database Independence**: Business logic remains separate from database implementation
5. **External Agency Independence**: Business logic is agnostic to external integrations

### ✨ Additional Features and Patterns

This project incorporates modern adaptations of Clean Architecture principles:

- **GraphQL vs HTTP**:  
  The `entrypoints` module offers both GraphQL and RESTful API interfaces

- **RelationalDB vs NoSQL**:  
  The `repositories` module supports both relational databases (SQLite, MySQL, PostgreSQL) and NoSQL options (MongoDB, Redis)

Additionally, the project implements:

- **Repository Pattern**:  
  Abstracts data storage from the model layer, promoting flexibility and maintainability

- **Unit of Work Pattern**:  
  Ensures transactional integrity across operations

- **Dependency Injection Pattern**:  
  Reduces direct dependencies between code modules, increasing testability

- **Asynchronous SQLalchemy**:  
  Utilizes SQLAlchemy 2.0's async capabilities for optimized database operations

## 🏗️ Architecture

This project follows clean architecture principles with distinct layers:

- **Models**: Domain entities and core business logic
- **Repositories**: Data access abstraction layer
- **Entrypoints**: API endpoints and request/response handling  
- **Mappers**: Conversion between API schemas and domain models

## 🧱 Project Structure Overview

Based on Uncle Bob's Clean Architecture principles, this project's structure and architecture flow diagrams are aligned with these principles.

#### Directory Structure

Here's a glimpse of the project's high-level structure, highlighting primary directories and key files:

```ini
./
├── ...
├── src/
│   ├── di/                   - Dependency injection configurations for managing dependencies.
│   │   ├── dependency_injection.py
│   │   └── unit_of_work.py
│   │
│   ├── entrypoints/          - External interfaces like HTTP & GraphQL endpoints.
│   │   ├── graphql/          - GraphQL components for a flexible API.
│   │   └── http/             - RESTful API routes and controllers.
│   │                           ('Frameworks and Drivers' and part of 'Interface Adapters' in Clean Architecture)
│   │
│   ├── usecases/             - Contains application-specific business rules and implementations.
│   │                           ('Use Cases' in Clean Architecture)
│   │
│   ├── repositories/         - Data interaction layer, converting domain data to/from database format.
│   │   ├── relational_db/    - Operations for relational databases (e.g., SQLite, MySQL, PostgreSQL).
│   │   ├── document_db/      - Operations for document-oriented databases (e.g., MongoDB, CouchDB).
│   │   └── key_value_db/     - Operations for key-value databases (e.g., Redis, Memcached).
│   │                           ('Interface Adapters' in Clean Architecture)
│   │
│   ├── models/               - Domain entities representing the business data.
│   │                           ('Entities' in Clean Architecture)
│   │
│   ├── common/               - Shared code and utilities.
│   ├── settings/
│   │   └── db/               - Database configurations.
│   │                           ('Frameworks and Drivers' in Clean Architecture)
│   │
│   └── main.py               - Main file to launch the application.
│
└── tests/
    ├── api_db_test.bats      - BATs tests for API and database interactions.
    ├── functional/           - Functional tests for testing the overall functionality and behavior of the application.
    ├── integration/          - Integration tests for testing module interactions.
    └── unit/                 - Unit tests for testing individual components in isolation.
```

