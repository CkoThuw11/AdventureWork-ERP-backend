# TinyBigCorp Backend

Python FastAPI backend following **Clean Architecture** principles.

## 🏗️ Architecture Layers

### Domain Layer (`src/domain/`)
The core of the application containing business logic and rules.
- **Entities**: Pure business objects (e.g., `User`)
- **Repository Interfaces**: Abstract contracts for data access (e.g., `IUserRepository`)
- **Exceptions**: Domain-specific exceptions

**Key Rule**: Domain layer has NO dependencies on other layers.

### Application Layer (`src/application/`)
Orchestrates the flow of data between Interface and Domain layers.
- **Services**: Business use cases (e.g., `UserService`)
- **DTOs**: Data Transfer Objects using Pydantic (e.g., `CreateUserCommand`, `UserDto`)

### Infrastructure Layer (`src/infrastructure/`)
Implements external dependencies and technical concerns.
- **Database**: SQLAlchemy models and connection management
- **Repositories**: Concrete implementations of repository interfaces
- **Logging**: Structlog configuration

### Interface Layer (`src/api/`)
Handles external communication (HTTP, CLI, etc.).
- **Routes**: FastAPI endpoints
- **Dependencies**: Dependency injection configuration
- **Main**: Application entry point with global exception handlers

## 🚀 Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/Mac
```

### 2. Install Dependencies
We use `pip` with `pyproject.toml` for dependency management. Install in editable mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

### 3. Setup Git Hooks
Initialize pre-commit hooks to automatically lint and format code before committing:

```bash
pre-commit install
```

### 4. Configure Environment
```bash
copy .env.example .env
# Edit .env with your configuration
```

### 5. Start Database
```bash
# From project root
docker-compose up -d
```

### 6. Run the Server
```bash
uvicorn src.api.main:app --reload
```

Server runs at: **http://localhost:8000**
- API Docs: **http://localhost:8000/docs**
- Health: **http://localhost:8000/health**

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_user_service.py
```

## 🔍 Code Quality

We use a suite of tools to maintain code quality. These run automatically via pre-commit, but you can run them manually:

### Linting & Formatting
**Ruff** handles both linting and import sorting. **Black** handles code formatting.

```bash
# Fix linting issues
ruff check . --fix

# Format code
black .
```

### Type Checking
We use **mypy** for static type checking.

```bash
mypy src/
```

### Run All Checks
```bash
pre-commit run --all-files
```

## 📝 Adding a New Feature

Follow the workflow from `AGENTS.md`:

1. **Database**: Write migration in `migrations/V{N}__description.sql`
2. **Domain**: Define entity and repository interface
3. **Application**: Create service and DTOs
4. **Infrastructure**: Implement repository
5. **Interface**: Create API routes

## 🗄️ Database Migrations

Migrations are located in `migrations/` and follow Flyway naming:
- `V1__initial_schema.sql`
- `V2__add_user_roles.sql`

The database is automatically initialized when using Docker Compose.

## 📚 Key Files

- `src/api/main.py` - Application entry point
- `src/api/dependencies.py` - Dependency injection
- `src/infrastructure/config.py` - Configuration management
- `pyproject.toml` - Project configuration and tool settings

## 🎯 Architecture Validation

**The Swap Test**: Change database by modifying only:
- `src/infrastructure/repositories/` implementations
- `src/api/dependencies.py` DI configuration

**The Junior Test**: A junior developer should understand the business by reading only `src/domain/`.
