# Book Review Service 📚

A high-performance RESTful API service for managing books and their reviews, built with FastAPI, PostgreSQL, and Redis caching.

## ✨ Features

- **Book Management**: Create and list books with validation
- **Review System**: Add and retrieve reviews for books
- **Performance Optimized**: Redis caching and database indexing
- **Robust Architecture**: Clean separation of concerns with service layer
- **Database Migrations**: Alembic for schema versioning
- **Comprehensive Testing**: Unit, integration, and end-to-end tests
- **Docker Support**: Containerized development and deployment
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL (SQLite for development)
- **Cache**: Redis 5.0.1
- **ORM**: SQLAlchemy 2.0.23
- **Migrations**: Alembic 1.12.1
- **Testing**: Pytest 7.4.3
- **Validation**: Pydantic 2.5.0

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/JxTIN21/Book-Review-Service.git
cd book-review-service

# Start all services
docker-compose up --build

# The API will be available at http://localhost:8000
```

### Option 2: Local Development

```bash
# Clone and navigate to project
git clone https://github.com/JxTIN21/Book-Review-Service.git
cd book-review-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn main:app --reload
```

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL (for production)
- Redis (optional, for caching)
- Docker & Docker Compose (for containerized setup)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/bookreviews
# For SQLite (development):
# DATABASE_URL=sqlite:///./book_reviews.db

# Redis Cache
REDIS_URL=redis://localhost:6379
CACHE_TTL=300

# Application
DEBUG=True
LOG_LEVEL=INFO
```

### Database Setup

#### PostgreSQL (Production)
```bash
# Create database
createdb bookreviews

# Set environment variable
export DATABASE_URL=postgresql://username:password@localhost:5432/bookreviews

# Run migrations
alembic upgrade head
```

#### SQLite (Development)
```bash
# SQLite database will be created automatically
# Default: sqlite:///./book_reviews.db
alembic upgrade head
```

## 🗄️ Database Migrations

### Running Migrations

```bash
# Upgrade to latest migration
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade to previous revision
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

### Creating New Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new field to Book model"

# Create empty migration
alembic revision -m "Custom migration description"
```

## 🧪 Testing

### Run All Tests
```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_books.py -v

# Run specific test function
pytest tests/test_books.py::test_create_book -v
```

### Test Categories

```bash
# Unit tests
pytest tests/test_books.py tests/test_reviews.py -v

# Integration tests
pytest tests/test_integration.py -v

# Cache service tests
pytest tests/test_cache_service.py -v

# Run tests with specific markers
pytest -m "not integration" -v  # Skip integration tests
```

### Test Database

Tests use an isolated SQLite database that's created and destroyed for each test session. No additional setup required.

## 📚 API Documentation

Once the service is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 API Endpoints

### Books
- `GET /books` - List all books (with pagination)
- `POST /books` - Create a new book

### Reviews
- `GET /books/{book_id}/reviews` - Get reviews for a book
- `POST /books/{book_id}/reviews` - Add a review to a book

### Health
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics (if monitoring enabled)

## 📝 Usage Examples

### Create a Book
```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "description": "A classic American novel",
    "published_year": 1925
  }'
```

### List Books
```bash
curl "http://localhost:8000/books?skip=0&limit=10"
```

### Add a Review
```bash
curl -X POST "http://localhost:8000/books/1/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_name": "John Doe",
    "rating": 4.5,
    "comment": "Excellent read!"
  }'
```

### Get Book Reviews
```bash
curl "http://localhost:8000/books/1/reviews"
```

## 🏗️ Project Structure

```
book-review-service/
├── main.py                    # FastAPI application entry point
├── database.py               # Database configuration
├── models.py                 # SQLAlchemy ORM models
├── schemas.py                # Pydantic request/response models
├── requirements.txt          # Python dependencies
├── alembic.ini              # Alembic configuration
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-service setup
│
├── services/                # Business logic layer
│   ├── book_service.py      # Book operations
│   ├── review_service.py    # Review operations
│   └── cache_service.py     # Redis caching
│
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   └── env.py              # Alembic environment
│
└── tests/                   # Test suite
    ├── conftest.py         # Test configuration
    ├── test_books.py       # Book endpoint tests
    ├── test_reviews.py     # Review endpoint tests
    ├── test_integration.py # Integration tests
    └── test_cache_service.py # Cache tests
```

## 🔧 Development Setup

### Database Reset
```bash
# Drop and recreate database (PostgreSQL)
dropdb bookreviews && createdb bookreviews
alembic upgrade head

# Or delete SQLite file
rm book_reviews.db
alembic upgrade head
```

### Seed Sample Data
```bash
# Run the seed script (if available)
python scripts/seed_data.py

# Or create via API
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Book", "author": "Sample Author"}'
```

## 🐳 Docker Commands

```bash
# Build and start services
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f api

# Run migrations in container
docker-compose exec api alembic upgrade head

# Run tests in container
docker-compose exec api pytest tests/ -v

# Stop services
docker-compose down

# Reset everything (remove volumes)
docker-compose down -v
```

## 🚀 Production Deployment

### Environment Setup
```bash
# Set production environment variables
export DATABASE_URL=postgresql://user:pass@prod-db:5432/bookreviews
export REDIS_URL=redis://prod-redis:6379
export DEBUG=False

# Run migrations
alembic upgrade head

# Start with production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Production
```bash
# Build production image
docker build -t book-review-service .

# Run production container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_URL=redis://redis-host:6379 \
  book-review-service
```

## 📊 Performance Features

- **Database Indexing**: Optimized queries with proper indexes
- **Redis Caching**: Automatic caching of frequently accessed data
- **Connection Pooling**: Efficient database connection management
- **Pagination**: Built-in pagination for large datasets
- **Async Operations**: Non-blocking I/O operations

## 🛡️ Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server errors

## 🧩 Extending the Service

### Adding New Endpoints
1. Create new router in `api/routers/`
2. Add business logic to `services/`
3. Update database models if needed
4. Create migration with `alembic revision --autogenerate`
5. Add tests in `tests/`

### Adding New Models
1. Define model in `models.py`
2. Create Pydantic schemas in `schemas.py`
3. Generate migration: `alembic revision --autogenerate -m "Add new model"`
4. Run migration: `alembic upgrade head`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest tests/ -v`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check if PostgreSQL is running
pg_isready

# Verify connection string
echo $DATABASE_URL
```

**Redis Connection Error**
```bash
# Check if Redis is running
redis-cli ping

# Should return PONG if working
```

**Migration Errors**
```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Reset to specific revision
alembic downgrade <revision_id>
```

**Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Getting Help

- Check the [API documentation](http://localhost:8000/docs) when the service is running
- Review the test files for usage examples
- Check Docker logs: `docker-compose logs -f api`
- Enable debug logging by setting `LOG_LEVEL=DEBUG`

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check existing issues for solutions
- Review the test suite for usage examples

---

**Happy coding! 🎉**