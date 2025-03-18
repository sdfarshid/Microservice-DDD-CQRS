# Product Publisher Channels (PPC)

## 🚧 Under Development

A microservices-based system that enables businesses to manage and sell products across multiple messaging platforms like Telegram and WhatsApp. Built with Domain-Driven Design (DDD) principles, this project demonstrates various implementation approaches for learning and practical purposes.

## 📝 About the Project

PPC is designed to help businesses reach their customers directly through popular messaging platforms. The system is built using a microservices architecture, with each service handling specific business domains.

### Microservices Architecture
- **User Service**: Authentication, authorization, and user management
- **Product Service**: Product and catalog management
- **Order Service**: Order processing and management
- **Company Service**: (Planned) Company management and settings

### Key Architectural Decisions
- Microservices architecture for scalability and maintainability
- Domain-Driven Design (DDD) principles
- Clean separation of concerns (API, Domain, Infrastructure)
- CQRS pattern (Commands and Queries)
- Event-driven architecture
- Repository pattern for data access

## 🏗 Project Structure

```
app/
├── api/                  # API Layer
│   └── v1/               # API Version 1
│       ├── endpoints/    # API Endpoints
│       └── routers.py    # Route Definitions
├── domain/              # Domain Layer
│   └── user/            # User Domain
│       ├── models/      # Domain Models
│       ├── commands/    # Command Handlers
│       ├── queries/     # Query Handlers
│       └── services/    # Domain Services
└── infrastructure/      # Infrastructure Layer
    ├── database/       # Database Access
    └── message_broker/ # Message Queue
```

## 🔧 Features

### Core Features

#### Product Management
- Product catalog management
- Product categories and attributes
- Pricing and inventory management
- Media management for product images

#### Channel Integration
- Telegram bot integration
- WhatsApp business API integration
- Multi-channel product publishing
- Channel-specific pricing and inventory

#### Order Management
- Order processing and tracking
- Order status updates
- Payment integration
- Order history and analytics

#### User & Authentication
- User registration and login
- JWT-based authentication
- Role-based access control
- Multi-tenant support

#### Company Management (Planned)
- Company profile management
- Business settings
- Channel configuration
- Analytics and reporting

## 🛠 Technologies

- **Backend Framework**: FastAPI
- **Database**: SQLAlchemy ORM
- **Message Broker**: RabbitMQ
- **Authentication**: JWT
- **Testing**: pytest
- **Containerization**: Docker & Kubernetes
- **API Documentation**: OpenAPI (Swagger)
- **Message Platforms**: Telegram Bot API, WhatsApp Business API

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run with Docker:
```bash
docker-compose up
```

## 🧪 Testing

The project includes both unit and integration tests:

```bash
python -m pytest tests/
```

## 📌 Note

This project is under active development and serves as a learning platform for various software development patterns and practices. Some implementations may vary in approach to demonstrate different architectural patterns.

## 📜 License

[Add your license type here]
