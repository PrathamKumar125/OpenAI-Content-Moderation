# Content Moderation Service

A scalable FastAPI-based service for content moderation using OpenAI's moderation API. The service provides real-time moderation of text and images with caching, metrics collection, and health monitoring capabilities.

## Features

- Text and image content moderation
- Redis-based caching for improved performance
- Celery-based asynchronous task processing
- Prometheus metrics integration
- Health monitoring for all service components
- Docker and Docker Compose support
- PostgreSQL for persistent storage

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API key

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/content-moderation-service.git
cd content-moderation-service
```

2. Create a `.env` file with your configuration:
```env
DATABASE_URL=postgresql://user:password@db:5432/content_moderation
POSTGRES_PASSWORD=your_password
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
OPENAI_API_KEY=your_openai_api_key
LOG_LEVEL=info
DEBUG=True
```

3. Build and start the services using Docker Compose:
```bash
# Build and start all services
docker-compose up --build

# Start services in detached mode
docker-compose up --build -d

# View logs when running in detached mode
docker-compose logs -f
```

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /health/ready` - Detailed readiness check of all components

### Content Moderation
- `POST /api/v1/moderate/text` - Moderate text content
- `POST /api/v1/moderate/image` - Moderate image content
- `GET /api/v1/moderate/{task_id}` - Get moderation result

### Metrics and Statistics
- `GET /api/v1/metrics` - Prometheus metrics
- `GET /api/v1/stats` - Service statistics

## Architecture

The service consists of the following components:

- FastAPI web server
- Celery workers for async processing
- Redis for caching and message broker
- PostgreSQL for persistent storage
- Prometheus for metrics collection

## Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
uvicorn main:app --reload
```

3. Start Celery worker:
```bash
celery -A services.celery worker --pool=solo --loglevel=info
```

## Testing

Run the test suite:
```bash
pytest
```

## Monitoring

Access the monitoring endpoints:

- FastAPI Swagger UI: http://localhost:8000/docs
- Prometheus metrics: http://localhost:9090
