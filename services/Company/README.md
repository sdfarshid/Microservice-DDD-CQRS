# Company Service

## Overview
The Company Service is a microservice built using Python and FastAPI, implementing Domain-Driven Design (DDD) and CQRS (Command Query Responsibility Segregation) patterns. It provides comprehensive company management functionality with a clean and maintainable architecture.

## Features
- Company management operations (CRUD)
- Asynchronous database operations
- Domain-driven design implementation
- Data validation and error handling
- Pagination support for company listings

## Architecture

### Domain-Driven Design (DDD)
The service follows DDD principles with clear separation of:
- **Domain Layer**: Contains business logic and domain models
- **Infrastructure Layer**: Handles database operations and external concerns
- **Application Layer**: Orchestrates use cases and workflow
- **Interface Layer**: Manages API endpoints and request/response handling

### CQRS Pattern
The service implements CQRS by separating:
- **Commands**: Operations that modify state (create, update, delete)
- **Queries**: Operations that read state (get, list)

## Core Components

### Repositories
- `CompanyRepository`: Implements data access patterns for company management
- Handles database operations using SQLAlchemy
- Includes error handling and transaction management

### Domain Models
- `Company`: Core domain entity representing company data
- Implements business rules and validations

### Service Handlers
The service provides the following operations:
1. **Create Company**
   - Add new company records
   - Validate company information
   - Ensure data integrity

2. **Read Operations**
   - Get company by ID
   - List companies with pagination
   - Find company by registration number

3. **Update Operations**
   - Modify existing company records
   - Partial updates supported

4. **Delete Operations**
   - Remove company records
   - Ensure proper cleanup

## Technical Stack
- **Framework**: FastAPI
- **Database**: SQLAlchemy (Async)
- **Data Mapping**: Custom mappers for ORM/Domain conversion
- **Error Handling**: Comprehensive error management with logging
- **Migrations**: Alembic for database schema management

## API Endpoints

### Company Management
- `POST /company` - Create new company
- `GET /company/{id}` - Retrieve company by ID
- `GET /company` - List companies (with pagination)
- `PUT /company/{id}` - Update company
- `DELETE /company/{id}` - Delete company
- `GET /company/registration/{number}` - Find company by registration number

## Error Handling
The service implements robust error handling:
- Database integrity errors
- Not found scenarios
- Validation errors
- Unexpected exceptions

## Project Structure
