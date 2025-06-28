#!/bin/bash

echo "Setting up Book Review Service..."

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize Alembic (if not already done)
if [ ! -d "alembic" ]; then
    alembic init alembic
fi

# Create database and run migrations
alembic upgrade head

# Run tests
echo "Running tests..."
pytest tests/ -v

echo "Setup complete!"
echo ""
echo "To start the development server:"
echo "  uvicorn main:app --reload"
echo ""
echo "To start with Docker:"
echo "  docker-compose up --build"
echo ""
echo "API Documentation will be available at:"
echo "  http://localhost:8000/docs (Swagger UI)"
echo "  http://localhost:8000/redoc (ReDoc)"