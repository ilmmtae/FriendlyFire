# FastAPI User Management Service

An asynchronous microservice dedicated to user lifecycle management, secure authentication, and authorization.

## ⚡️ Key Features
* **Asynchronous Architecture:** Built with `asyncio` for efficient concurrency.
* **JWT Authentication:** OAuth2 implementation with Access & Refresh token rotation.
* **Security:** Password hashing using `bcrypt` and protection via **Redis** rate limiting.
* **Automated Workflows:** Background tasks for Email verification and system notifications.
* **Data Validation:** Robust schema enforcement using **Pydantic V2**.

## 🛠 Tech Stack
* **Framework:** FastAPI
* **Database:** PostgreSQL (Async SQLAlchemy)
* **Migrations:** Alembic
* **Cache/Security:** Redis
* **Containerization:** Docker & Docker Compose

## 🚀 Getting Started
1. Configure your `.env` file based on `.env.example`.
2. Run the service:
   ```bash
   docker-compose up --build 
