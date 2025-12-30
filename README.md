# Face Recognition Server

A high-performance face recognition server built with FastAPI, PostgreSQL with pgvector, and InsightFace.

## Features

- Face detection
- Face feature extraction
- Face search and matching
- Application management
- Local and cloud storage support
- Docker containerization

## Technology Stack

- Python 3.8+
- FastAPI
- PostgreSQL + pgvector
- Docker & Docker Compose
- InsightFace
- uv (local development) / pip (Docker deployment)

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- uv (Python package manager)

### Using Docker Compose

1. Clone the repository
2. Copy `.env.example` to `.env` and adjust settings
3. Start services:

```bash
docker-compose up -d
```

4. Run database migrations:

```bash
docker-compose exec face-server alembic upgrade head
```

5. Access the API at http://localhost:8000
6. View API documentation at http://localhost:8000/docs

### Local Development

1. Install uv (for local development):

```bash
pip install uv
```

2. Create virtual environment and install dependencies:

```bash
uv venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
uv pip install -e .
```

3. Start PostgreSQL (via Docker):

```bash
docker-compose up postgres -d
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Applications

- `POST /api/v1/applications` - Create application
- `GET /api/v1/applications` - List applications
- `GET /api/v1/applications/{app_id}` - Get application
- `PUT /api/v1/applications/{app_id}` - Update application
- `DELETE /api/v1/applications/{app_id}` - Delete application

### Faces

- `POST /api/v1/faces` - Register face
- `GET /api/v1/faces` - List faces
- `GET /api/v1/faces/{face_id}` - Get face
- `DELETE /api/v1/faces/{face_id}` - Delete face
- `POST /api/v1/faces/search` - Search faces

## Project Structure

```
face-server/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API routes
│   ├── services/            # Business logic
│   └── core/                # Core modules (face detection, etc.)
├── alembic/                 # Database migrations
├── docs/                    # Documentation
├── tests/                   # Tests
├── storage/                 # Local file storage
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## License

MIT
