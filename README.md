# Grocery Tracker - Smart OCR/LLM-based Order Recording System

![Grocery Tracker]

## Overview
The **Grocery Tracker** is a smart application that utilizes OCR (Optical Character Recognition) and LLM (Large Language Model) capabilities to automatically extract order details from uploaded receipts. This data is used to track spending patterns and analyze financial habits. The system also includes budget alerts to notify users when they exceed their weekly or monthly spending limits.

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy with Alembic for migrations
- **Authentication:** JWT (JSON Web Token)
- **AI Processing:** OpenAI GPT-4 Vision API
- **Dependency Management:** PDM (Python Dependency Manager)
- **Containerization:** Docker & Docker Compose
- **Infrastructure:** pgAdmin for database management

---

## Features

- **Order Upload:** Upload order screenshots to extract structured data.
- **Spending Analytics:** Analyze spending patterns by category, platform, and payment method.
- **Authentication:** Secure JWT-based authentication.
- **RESTful APIs:** For seamless integrations and data retrieval.

---

## Installation and Running the Project Locally

### Prerequisites

Ensure you have the following installed:

- Python (>= 3.11)
- PDM (Python Dependency Manager)
- Docker and Docker Compose

### Setup Instructions

#### 1. Clone the Repository
```bash
$ git clone https://github.com/rishabjn10/Grocery-Tracker.git
$ cd grocery-tracker
```

#### 2. Install Dependencies

Install PDM if not installed:
```bash
$ curl -sSL https://pdm.fming.dev/install-pdm.py | python3
```

Install project dependencies:
```bash
$ pdm install
```

#### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add the following:
```env
DATABASE_URL=postgresql://root:root@localhost:5432/grocery_tracker_database
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 4. Run Database Migrations
```bash
$ pdm run alembic upgrade head
```

#### 5. Run the Server Locally

```bash
$ pdm install
$ pdm run alembic upgrade head
$ pdm run python main.py
```

The server will be running at `http://localhost:8000`

Access the interactive API documentation at:
- [Swagger UI](http://localhost:8000/docs)
- [Redoc](http://localhost:8000/redoc)

---

## Running with Docker

### 1. Deploy PostgreSQL Database Locally

```bash
$ docker-compose up -d
```

### 2. Run FastAPI Server Locally

```bash
$ pdm install
$ pdm run alembic upgrade head
$ pdm run python main.py
```

### 3. Access the Services

- **FastAPI Application:** `http://localhost:8000`
- **pgAdmin Dashboard:** `http://localhost:5050` (Login with email: `admin@admin.com` password: `root`)

---

## Production Deployment

For production usage, the database would be hosted remotely. To deploy the FastAPI application:

1. Comment out the `db` service lines in `docker-compose.yml`.
2. Uncomment the `fastapi_grocery_tracker` service.
3. Run the following command:

```bash
$ docker-compose up -d
```

---

POSTMAN collection - ```https://documenter.getpostman.com/view/20933055/2sAYQfEpVv```

