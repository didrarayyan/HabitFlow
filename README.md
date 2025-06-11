# HabitFlow - Daily Habit Tracker

<div align="center">
  <img src="https://via.placeholder.com/120x120/3B82F6/FFFFFF?text=⚡" alt="HabitFlow Logo" width="120" height="120">
  
  <h3>Build Better Habits, Track Your Progress</h3>
  
  <p>A modern, full-stack habit tracking application with cloud sync, analytics, and beautiful UI</p>
  
  [![CI/CD](https://github.com/didrarayyan/HabitFlow/workflows/HabitFlow%20CI/CD/badge.svg)](https://github.com/didrarayyan/HabitFlow/actions)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![Node.js 20+](https://img.shields.io/badge/node.js-20+-green.svg)](https://nodejs.org/)
  [![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
</div>

## ✨ Features

### 🎯 Core Functionality
- **Habit Management**: Create, edit, and delete daily habits with customizable icons and colors
- **Daily Check-ins**: Mark habits as complete with support for boolean, count, and duration tracking
- **Streak Tracking**: Monitor current and longest streaks to maintain motivation
- **Progress Analytics**: Visualize your progress with interactive charts and statistics

### 📊 Analytics & Insights
- **Dashboard Overview**: Get a quick snapshot of today's progress and overall statistics
- **Detailed Analytics**: View completion rates, trends, and performance over time
- **Calendar Heatmap**: Visual representation of habit completion patterns
- **Progress Charts**: Line and bar charts showing habit performance over different time periods

### 🔐 Authentication & Security
- **User Registration & Login**: Secure email/password authentication
- **JWT Token Management**: Access and refresh token system
- **Password Security**: Bcrypt hashing for secure password storage
- **OAuth Integration**: Ready for Google OAuth integration

### 🎨 User Experience
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark/Light Mode**: Toggle between themes based on user preference
- **Intuitive Interface**: Clean, modern UI built with Tailwind CSS and shadcn/ui
- **Real-time Updates**: Instant feedback and updates across the application

### ☁️ Cloud & Sync
- **Data Export/Import**: Export your data in CSV/JSON format
- **Google Sheets Integration**: Sync your habits to Google Sheets (configurable)
- **Backup & Restore**: Secure data backup and restoration capabilities

### 🔧 Technical Features
- **RESTful API**: Well-documented FastAPI backend with automatic OpenAPI documentation
- **Database Support**: PostgreSQL for production, SQLite for development
- **Caching**: Redis integration for improved performance
- **Background Tasks**: Celery integration for email notifications and data processing
- **Docker Support**: Complete containerization for easy deployment
- **CI/CD Pipeline**: Automated testing, building, and deployment with GitHub Actions



## 🏗️ Architecture

HabitFlow follows a modern full-stack architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React TS)    │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
│                 │    │                 │    │                 │
│ • React 18      │    │ • Python 3.11+ │    │ • PostgreSQL 15 │
│ • TypeScript    │    │ • FastAPI       │    │ • Redis Cache   │
│ • Tailwind CSS  │    │ • SQLAlchemy    │    │                 │
│ • Recharts      │    │ • Pydantic      │    │                 │
│ • React Router  │    │ • JWT Auth      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Backend Stack
- **Framework**: FastAPI with async/await support
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic models for request/response validation
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Testing**: Pytest with coverage reporting

### Frontend Stack
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **Charts**: Recharts for data visualization
- **Routing**: React Router for client-side navigation
- **State Management**: Context API with useReducer
- **HTTP Client**: Fetch API with custom hooks

### Infrastructure
- **Containerization**: Docker and Docker Compose
- **Reverse Proxy**: Nginx for production deployment
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Monitoring**: Health checks and logging
- **SSL**: Let's Encrypt integration for HTTPS

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Python** (3.11+) for local development
- **Node.js** (20+) and **pnpm** for frontend development
- **Git** for version control

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/didrarayyan/HabitFlow.git
   cd HabitFlow
   ```

2. **Run the setup script**
   ```bash
   ./scripts/setup-dev.sh
   ```

3. **Start the application**
   ```bash
   docker-compose -f infra/docker-compose.yml up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

1. **Clone and setup**
   ```bash
   git clone https://github.com/didrarayyan/HabitFlow.git
   cd HabitFlow
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend setup** (in a new terminal)
   ```bash
   cd frontend
   pnpm install
   pnpm run dev
   ```

4. **Database setup** (optional - uses SQLite by default)
   ```bash
   # Start PostgreSQL and Redis with Docker
   docker-compose -f infra/docker-compose.yml up -d postgres redis
   ```


## 📁 Project Structure

```
HabitFlow/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Core configuration and utilities
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic schemas for validation
│   │   ├── services/       # Business logic and database operations
│   │   └── tests/          # Backend tests
│   ├── main.py             # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── contexts/       # React context providers
│   │   ├── pages/          # Page components
│   │   └── assets/         # Static assets
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container configuration
├── infra/                  # Infrastructure and deployment
│   ├── docker-compose.yml  # Multi-service orchestration
│   ├── nginx/              # Nginx configuration
│   └── .env.production     # Production environment variables
├── scripts/                # Deployment and utility scripts
│   ├── setup-dev.sh        # Development environment setup
│   └── deploy-prod.sh      # Production deployment
├── .github/workflows/      # CI/CD pipeline configuration
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

#### Backend Configuration (.env)
```bash
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=habitflow
POSTGRES_PASSWORD=habitflow123
POSTGRES_DB=habitflow
USE_SQLITE=true  # Set to false for PostgreSQL

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=480

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Google API (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

#### Frontend Configuration (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=HabitFlow
VITE_APP_VERSION=1.0.0
```

### Database Setup

#### PostgreSQL (Production)
```bash
# Using Docker
docker run -d \
  --name habitflow-postgres \
  -e POSTGRES_DB=habitflow \
  -e POSTGRES_USER=habitflow \
  -e POSTGRES_PASSWORD=habitflow123 \
  -p 5432:5432 \
  postgres:15-alpine

# Or using Docker Compose
docker-compose -f infra/docker-compose.yml up -d postgres
```

#### SQLite (Development)
SQLite is used by default for development. The database file will be created automatically at `backend/habitflow.db`.

## 📚 API Documentation

The API is automatically documented using FastAPI's built-in OpenAPI support.

### Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key API Endpoints

#### Authentication
```bash
POST /api/v1/auth/register     # User registration
POST /api/v1/auth/login        # User login
POST /api/v1/auth/refresh      # Refresh access token
```

#### Users
```bash
GET  /api/v1/users/me          # Get current user
PUT  /api/v1/users/me          # Update current user
```

#### Habits
```bash
GET    /api/v1/habits/         # List user habits
POST   /api/v1/habits/         # Create new habit
GET    /api/v1/habits/{id}     # Get specific habit
PUT    /api/v1/habits/{id}     # Update habit
DELETE /api/v1/habits/{id}     # Delete habit
```

#### Habit Entries
```bash
GET  /api/v1/habits/entries/date/{date}  # Get entries for date
POST /api/v1/habits/entries              # Create habit entry
PUT  /api/v1/habits/entries/{id}         # Update habit entry
```

#### Analytics
```bash
GET /api/v1/analytics/dashboard          # Dashboard statistics
GET /api/v1/analytics/habits             # Habit analytics
GET /api/v1/analytics/habits/{id}/calendar  # Calendar data
```

### Example API Usage

#### Create a New Habit
```bash
curl -X POST "http://localhost:8000/api/v1/habits/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Drink Water",
    "description": "Drink 8 glasses of water daily",
    "habit_type": "count",
    "target_value": 8,
    "unit": "glasses",
    "icon": "💧",
    "color": "#3B82F6"
  }'
```

#### Mark Habit as Complete
```bash
curl -X POST "http://localhost:8000/api/v1/habits/entries" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "habit_id": 1,
    "date": "2024-01-15",
    "completed": true,
    "value": 8
  }'
```


## 🚀 Deployment

### Production Deployment

#### Option 1: Using Deployment Script
```bash
# Set your domain and email
export DOMAIN=your-domain.com
export EMAIL=admin@your-domain.com

# Run the deployment script
./scripts/deploy-prod.sh
```

#### Option 2: Manual Docker Deployment
```bash
# 1. Clone the repository on your server
git clone https://github.com/didrarayyan/HabitFlow.git
cd HabitFlow

# 2. Configure production environment
cp infra/.env.production infra/.env
# Edit infra/.env with your production settings

# 3. Build and start services
docker-compose -f infra/docker-compose.yml --env-file infra/.env up -d --build

# 4. Setup SSL (optional)
# Configure your reverse proxy (nginx, traefik, etc.) for SSL termination
```

#### Option 3: Cloud Deployment

##### Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set POSTGRES_SERVER=your-postgres-host
# ... other environment variables

# Deploy
git push heroku main
```

##### DigitalOcean App Platform
1. Fork this repository
2. Connect your GitHub account to DigitalOcean
3. Create a new app and select your forked repository
4. Configure environment variables in the app settings
5. Deploy!

##### AWS/GCP/Azure
Use the provided Docker containers with your preferred container orchestration service (ECS, Cloud Run, Container Instances).

### Environment-Specific Configurations

#### Development
- Uses SQLite database
- CORS allows localhost origins
- Debug mode enabled
- Hot reloading for both frontend and backend

#### Staging
- Uses PostgreSQL database
- Limited CORS origins
- Production-like environment for testing
- SSL certificates (Let's Encrypt staging)

#### Production
- PostgreSQL with connection pooling
- Redis for caching and sessions
- SSL certificates (Let's Encrypt production)
- Nginx reverse proxy
- Log rotation and monitoring
- Automated backups

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_auth.py -v

# Run tests with database
pytest app/tests/ -v --db-url=postgresql://user:pass@localhost/test_db
```

### Frontend Tests
```bash
cd frontend

# Install dependencies
pnpm install

# Run unit tests
pnpm run test

# Run tests with coverage
pnpm run test:coverage

# Run e2e tests (if configured)
pnpm run test:e2e

# Lint code
pnpm run lint

# Type checking
pnpm run type-check
```

### Integration Tests
```bash
# Start test environment
docker-compose -f infra/docker-compose.yml -f infra/docker-compose.test.yml up -d

# Run integration tests
pytest integration_tests/

# Cleanup
docker-compose -f infra/docker-compose.yml -f infra/docker-compose.test.yml down
```

## 🔍 Monitoring and Logging

### Application Monitoring
- Health check endpoints for all services
- Structured logging with correlation IDs
- Performance metrics collection
- Error tracking and alerting

### Log Management
```bash
# View application logs
docker-compose -f infra/docker-compose.yml logs -f

# View specific service logs
docker-compose -f infra/docker-compose.yml logs -f backend
docker-compose -f infra/docker-compose.yml logs -f frontend

# Export logs
docker-compose -f infra/docker-compose.yml logs --no-color > habitflow.log
```

### Database Monitoring
```bash
# Connect to PostgreSQL
docker-compose -f infra/docker-compose.yml exec postgres psql -U habitflow -d habitflow

# View database size
SELECT pg_size_pretty(pg_database_size('habitflow'));

# Monitor active connections
SELECT count(*) FROM pg_stat_activity;
```

## 🛠️ Development

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/didrarayyan/HabitFlow.git
   cd HabitFlow
   ```

2. **Install development tools**
   ```bash
   # Backend tools
   pip install black isort flake8 mypy pytest

   # Frontend tools
   npm install -g pnpm
   pnpm install
   ```

3. **Setup pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Code Style and Standards

#### Backend (Python)
- **Formatter**: Black with line length 88
- **Import sorting**: isort
- **Linting**: flake8
- **Type checking**: mypy
- **Docstrings**: Google style

```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/
```

#### Frontend (TypeScript/React)
- **Formatter**: Prettier
- **Linting**: ESLint with TypeScript rules
- **Type checking**: TypeScript compiler

```bash
# Format and lint
pnpm run lint
pnpm run format

# Type checking
pnpm run type-check
```

### Database Migrations

#### Creating Migrations
```bash
cd backend

# Generate migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head

# Downgrade migration
alembic downgrade -1
```

#### Migration Best Practices
- Always review auto-generated migrations
- Test migrations on a copy of production data
- Include both upgrade and downgrade paths
- Document breaking changes

### Adding New Features

1. **Create a feature branch**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Backend development**
   - Add models in `app/models/`
   - Create schemas in `app/schemas/`
   - Implement services in `app/services/`
   - Add API endpoints in `app/api/`
   - Write tests in `app/tests/`

3. **Frontend development**
   - Create components in `src/components/`
   - Add pages in `src/pages/`
   - Update contexts if needed
   - Add tests

4. **Testing**
   ```bash
   # Test backend
   cd backend && pytest

   # Test frontend
   cd frontend && pnpm run test
   ```

5. **Submit pull request**
   - Ensure all tests pass
   - Update documentation
   - Follow commit message conventions


## 🤝 Contributing

We welcome contributions to HabitFlow! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Add tests** for new functionality
5. **Ensure all tests pass**
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to the branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Contribution Guidelines

- **Code Quality**: Follow the established code style and standards
- **Testing**: Add tests for new features and bug fixes
- **Documentation**: Update documentation for API changes
- **Commit Messages**: Use clear, descriptive commit messages
- **Pull Requests**: Provide detailed descriptions of changes

### Types of Contributions

- 🐛 **Bug fixes**
- ✨ **New features**
- 📚 **Documentation improvements**
- 🎨 **UI/UX enhancements**
- ⚡ **Performance optimizations**
- 🧪 **Test coverage improvements**

### Development Workflow

1. **Check existing issues** before starting work
2. **Create an issue** for new features or bugs
3. **Discuss the approach** in the issue comments
4. **Implement the solution** following our guidelines
5. **Submit a pull request** with detailed description

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues

**Database Connection Error**
```bash
# Check if PostgreSQL is running
docker-compose -f infra/docker-compose.yml ps postgres

# Check database logs
docker-compose -f infra/docker-compose.yml logs postgres

# Reset database
docker-compose -f infra/docker-compose.yml down -v
docker-compose -f infra/docker-compose.yml up -d postgres
```

**Import Errors**
```bash
# Ensure you're in the correct directory and virtual environment
cd backend
source venv/bin/activate
export PYTHONPATH=/path/to/backend
```

**Authentication Issues**
```bash
# Check JWT secret key configuration
echo $SECRET_KEY

# Verify token expiration settings
grep TOKEN_EXPIRE .env
```

#### Frontend Issues

**Build Errors**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
pnpm install

# Clear build cache
pnpm run clean
pnpm run build
```

**API Connection Issues**
```bash
# Check API URL configuration
cat frontend/.env

# Verify backend is running
curl http://localhost:8000/health
```

#### Docker Issues

**Container Won't Start**
```bash
# Check container logs
docker-compose -f infra/docker-compose.yml logs [service-name]

# Rebuild containers
docker-compose -f infra/docker-compose.yml build --no-cache

# Reset everything
docker-compose -f infra/docker-compose.yml down -v
docker system prune -a
```

**Port Conflicts**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Use different ports
docker-compose -f infra/docker-compose.yml up -d -p 8001:8000
```

### Getting Help

- 📖 **Documentation**: Check this README and API docs
- 🐛 **Issues**: Search existing GitHub issues
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Email**: Contact maintainers for security issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 HabitFlow Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **React** - A JavaScript library for building user interfaces
- **Tailwind CSS** - A utility-first CSS framework
- **shadcn/ui** - Beautifully designed components
- **PostgreSQL** - The world's most advanced open source database
- **Docker** - Containerization platform
- **GitHub Actions** - CI/CD platform

## 📞 Support

If you like this project, please consider:

- ⭐ **Starring** the repository
- 🐛 **Reporting bugs** via GitHub Issues
- 💡 **Suggesting features** via GitHub Discussions
- 🤝 **Contributing** to the codebase
- 📢 **Sharing** with others who might find it useful

---

<div align="center">
  <p>Made with ❤️ by the HabitFlow team</p>
  <p>
    <a href="https://github.com/didrarayyan/HabitFlow">GitHub</a> •
    <a href="https://habitflow.com">Website</a> •
    <a href="https://docs.habitflow.com">Documentation</a> •
    <a href="https://twitter.com/habitflow">Twitter</a>
  </p>
</div>
