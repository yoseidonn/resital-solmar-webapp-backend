# FastAPI Backend Template

## Features
- FastAPI application
- SQLite database with SQLAlchemy ORM
- Modular structure: models, schemas, routes

## Getting Started

### 1. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 2. Initialize the database
```python
# Run this in a Python shell:
from database import Base, engine
from models import User
Base.metadata.create_all(bind=engine)
```

### 3. Run the server
```bash
uvicorn main:app --reload
```

### 4. Test endpoints
- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs. 