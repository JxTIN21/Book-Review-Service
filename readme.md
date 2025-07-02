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
venv\Scripts\Activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn main:app --reload
```

---

## 🌐 Frontend (React)

The project now includes a user-friendly frontend built with **React** (Create React App).

### ✨ Frontend Features

- **Authentication**: User login and signup
- **Book Listing**: View all books with details
- **Review System**: Submit and view reviews
- **Modern UI**: Clean and responsive interface using Tailwind CSS
- **Routing**: Protected and public routes using React Router v6

## 🔐 Authentication (Login & Signup)

- **Login**: Users can log in with email and password
- **Signup**: New users can register using signup form
- **Token Management**: JWT is securely stored and used for protected API requests
- **Redirects**: Unauthenticated users are redirected to login

## 💻 Running the Frontend

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start the frontend server
npm start

# App runs at http://localhost:3000
```

...
**Happy coding! 🎉**
