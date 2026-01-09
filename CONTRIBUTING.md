# Contributing to Backend (AdventureWork-ERP-backend)

This guide is specific to backend development. For general contribution guidelines, see the [main repo CONTRIBUTING.md](https://github.com/CkoThuw11/TinyBigCorp/blob/main/CONTRIBUTING.md).

---

## 🚀 Quick Start

### Setup

```bash
# From main repo
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env
```

### Run Locally

```bash
# Start database (from main repo root)
cd ..
docker-compose up postgres -d

# Run backend
cd backend
uvicorn src.api.main:app --reload
```

---

## 🏗️ Clean Architecture Layers

### 1. Domain Layer (`src/domain/`)

**Pure business logic** - No dependencies on frameworks or infrastructure.

```python
# src/domain/entities/user.py
@dataclass
class User:
    id: Optional[int]
    email: str
    username: str

    def deactivate(self) -> None:
        """Business rule: Users can be deactivated."""
        self.is_active = False
```

**Rules**:
- ✅ Only Python standard library imports
- ✅ Business logic only
- ❌ No SQLAlchemy, FastAPI, or external libraries

### 2. Application Layer (`src/application/`)

**Use case orchestration** - Coordinates domain entities and repositories.

```python
# src/application/services/user_service.py
class UserService:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    async def create_user(self, command: CreateUserCommand) -> UserDto:
        # Orchestrate the use case
        user = User(...)
        created = await self._user_repo.create(user)
        return UserDto.model_validate(created)
```

**Rules**:
- ✅ Depends on Domain layer only
- ✅ Uses repository interfaces (not implementations)
- ❌ No HTTP knowledge
- ❌ No database knowledge

### 3. Infrastructure Layer (`src/infrastructure/`)

**Technical implementations** - Database, external APIs, etc.

```python
# src/infrastructure/repositories/user_repository.py
class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> User:
        # Map to ORM model
        model = UserModel(...)
        self._session.add(model)
        await self._session.commit()
        return self._to_entity(model)
```

**Rules**:
- ✅ Implements Domain interfaces
- ✅ Contains all technical details
- ❌ No business logic

### 4. Interface Layer (`src/api/`)

**HTTP routes** - Translates between HTTP and application.

```python
# src/api/routes/users.py
@router.post("/", response_model=UserDto)
async def create_user(
    command: CreateUserCommand,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.create_user(command)
```

**Rules**:
- ✅ Parse HTTP requests
- ✅ Call services
- ✅ Handle HTTP errors
- ❌ No business logic

---

## ✅ Code Quality

### Before Every Commit

```bash
# Run all checks
./scripts/check.sh

# Or manually:
ruff check .
black .
mypy src/
pytest --cov=src --cov-report=term-missing
```

### Linting Rules

- **Ruff**: Fast Python linter
- **Black**: Code formatter (line length: 100)
- **MyPy**: Type checker (strict mode)

### Testing Requirements

- ✅ Coverage > 80%
- ✅ Unit tests for all services
- ✅ Integration tests for repositories
- ✅ Test both success and error cases

---

## 🗄️ Database Migrations

### Creating Migrations

```bash
# Create new file: backend/migrations/V<number>__<description>.sql
# Example: V2__add_products.sql

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_name ON products(name);
```

### Migration Rules

1. **Sequential numbering**: V1, V2, V3...
2. **Descriptive names**: `V2__add_products.sql`
3. **Use transactions**: Wrap in BEGIN/COMMIT
4. **Test locally**: Before pushing
5. **Never modify**: Applied migrations are immutable

### Testing Migrations

```bash
# From main repo root
docker-compose down -v
docker-compose up postgres flyway

# Verify
docker exec -it tinybigcorp-postgres psql -U postgres -d tinybigcorp -c "\dt"
```

---

## 📝 Adding New Features

### Example: Add Product Entity

**1. Migration** (`migrations/V2__add_products.sql`)
```sql
CREATE TABLE products (...);
```

**2. Domain Entity** (`src/domain/entities/product.py`)
```python
@dataclass
class Product:
    id: Optional[int]
    name: str
    price: Decimal
```

**3. Repository Interface** (`src/domain/repositories/product_repository.py`)
```python
class IProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass
```

**4. DTOs** (`src/application/dtos/product_dto.py`)
```python
class CreateProductCommand(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., gt=0)
```

**5. Service** (`src/application/services/product_service.py`)
```python
class ProductService:
    async def create_product(self, command: CreateProductCommand) -> ProductDto:
        # Business logic
        pass
```

**6. Repository Implementation** (`src/infrastructure/repositories/product_repository.py`)
```python
class ProductRepository(IProductRepository):
    async def create(self, product: Product) -> Product:
        # Database logic
        pass
```

**7. API Routes** (`src/api/routes/products.py`)
```python
@router.post("/", response_model=ProductDto)
async def create_product(...):
    pass
```

---

## 🧪 Testing Examples

### Unit Test (No Database)

```python
# tests/unit/test_user_service.py
class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = []

    async def create(self, user: User) -> User:
        user.id = len(self.users) + 1
        self.users.append(user)
        return user

async def test_create_user():
    repo = InMemoryUserRepository()
    service = UserService(repo)

    command = CreateUserCommand(
        email="test@example.com",
        username="testuser",
        full_name="Test User"
    )

    result = await service.create_user(command)

    assert result.email == "test@example.com"
    assert len(repo.users) == 1
```

### Integration Test (With Database)

```python
# tests/integration/test_user_repository.py
async def test_user_repository_create(db_session):
    repo = UserRepository(db_session)

    user = User(
        id=None,
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    created = await repo.create(user)

    assert created.id is not None
    assert created.email == "test@example.com"
```

---

## 📋 PR Checklist

Before submitting a PR:

- [ ] Follows Clean Architecture layers
- [ ] All tests pass (`pytest`)
- [ ] Linting passes (`ruff`, `black`, `mypy`)
- [ ] Coverage > 80%
- [ ] Migration tested (if applicable)
- [ ] Documentation updated
- [ ] No business logic in routes
- [ ] Proper error handling
- [ ] Type hints on all functions

---

## 🚫 Common Mistakes

### ❌ Business Logic in Routes

```python
# BAD
@router.post("/users")
async def create_user(data: dict):
    if not data.get("email"):
        raise HTTPException(400)
    user = UserModel(email=data["email"])
    db.add(user)
    db.commit()
```

### ✅ Business Logic in Service

```python
# GOOD
@router.post("/users")
async def create_user(
    command: CreateUserCommand,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.create_user(command)
```

---

## 📚 Resources

- [Main Contributing Guide](https://github.com/CkoThuw11/TinyBigCorp/blob/main/CONTRIBUTING.md)
- [Learning Guides](https://github.com/CkoThuw11/TinyBigCorp/tree/main/docs)
- [Clean Architecture Guide](https://github.com/CkoThuw11/TinyBigCorp/blob/main/docs/02-clean-architecture.md)
- [SOLID Principles](https://github.com/CkoThuw11/TinyBigCorp/blob/main/docs/03-solid-principles.md)

---

**Questions?** Open a discussion in the main repo or tag `@anhhoangdev`.
