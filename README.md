# Content Moderation Service

FastAPI-based content moderation service using OpenAI's API for real-time text and image moderation.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Examples](#examples)
- [Development](#development)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Testing](#testing)
- [Performance](#performance)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

Key Features:
- Real-time content moderation
- Caching and performance optimization
- Scalable architecture
- Comprehensive monitoring
- Docker support

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   FastAPI   │────>│   Celery    │────>│   OpenAI    │
│   Server    │     │   Workers   │     │    API      │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       │            ┌─────────────┐
       └──────────>│   Redis     │
                   │   Cache     │
                   └─────────────┘
```

Components:
- FastAPI application server
- Redis for caching and message queue
- Celery for async processing
- PostgreSQL for data persistence
- Prometheus for metrics

## Getting Started

### Prerequisites
- Python 3.11+
- Redis
- PostgreSQL
- OpenAI API key

### Installation
```bash
git clone https://github.com/PrathamKumar125/content-moderation-service.git
cd content-moderation-service
pip install -r requirements.txt
```

### Configuration
Create `.env` file:
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

## Usage

### API Endpoints

#### Content Moderation
```
POST /api/v1/moderate/text
POST /api/v1/moderate/image
GET  /api/v1/moderate/{task_id}
```

#### Health & Metrics
```
GET /health
GET /metrics
```

### Examples

Text Moderation:
```bash
curl -X POST http://localhost:8000/api/v1/moderate/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Content to moderate"}'
```

## Development

### Local Setup
```bash
# Start services
redis-server
uvicorn main:app --reload
celery -A worker worker --loglevel=info
```

### Docker Setup
```bash
docker-compose up --build
```

## Testing

```bash
# Unit tests
pytest tests/unit

# Integration tests
pytest tests/integration

# Load tests
pytest tests/test_load.py
```

## Performance

Benchmarks:
- Response Time: < 500ms (p95)
- Throughput: 1000 req/s
- Concurrent Users: 50+

Optimization:
- Redis caching
- Connection pooling
- Async processing
- Rate limiting

## Monitoring

Metrics:
- Request latency
- Error rates
- Cache hit ratio
- Queue length
- Worker status

Tools:
- Prometheus
- Grafana dashboards
- Health checks

## Troubleshooting

Common Issues:
- Rate limiting: Implement backoff
- Cache misses: Adjust TTL
- Worker overload: Scale horizontally

Error Responses:
```json
{
    "error": "rate_limit_exceeded",
    "message": "Too many requests",
    "retry_after": 60
}
```
