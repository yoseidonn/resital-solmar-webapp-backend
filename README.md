# Resital Solmar Backend (FastAPI + Tortoise ORM)

This is the backend for the Resital Solmar villa/caretaker management system. It is built with **FastAPI** and **Tortoise ORM**, providing a modular, type-safe, and modern API for villa, caretaker, and report management.

---

## Features
- FastAPI application with automatic OpenAPI docs
- Tortoise ORM with SQLite (easy to switch to Postgres/MySQL)
- Modular structure: models, schemas, services, routes
- File upload/download for reports and outputs
- Output/report generation for APIS, Caretaker Extras View, and Extras Filtered Reservation
- Type-safe, Pydantic-based API responses
- CORS enabled for local frontend development

---

## Getting Started

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn main:app --reload
```

- The API will be available at [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Database
- Uses SQLite by default (`db.sqlite3`).
- Tortoise ORM auto-generates tables on startup.
- To reset, just delete `db.sqlite3` and restart the server.

---

## Main API Endpoints

| Path Prefix                              | Description                                 |
|------------------------------------------|---------------------------------------------|
| `/caretakers`                            | Caretaker CRUD                              |
| `/villas`                                | Villa CRUD                                  |
| `/resort-report-files`                   | Resort report file upload/CRUD              |
| `/resort-reports`                        | Resort report CRUD                          |
| `/apis-report-files`                     | APIS report file upload/CRUD                |
| `/advanced-passenger-information`        | Advanced passenger info CRUD                |
| `/caretaker-extras-view-outputs`         | Caretaker-specific extras view outputs       |
| `/apis-report-outputs`                   | APIS report outputs (generate/download)     |
| `/extras-filtered-reservation-outputs`   | Extras-based reservation outputs            |

All endpoints are fully documented in `/docs`.

---

## Project Structure

```
backend/
  main.py                # FastAPI app entrypoint
  models/                # Tortoise ORM models
  schemas/               # Pydantic schemas
  services/              # Business logic/services
  routes/                # API route modules
  media/                 # Uploaded/generated files
  requirements.txt       # Python dependencies
  db.sqlite3             # SQLite database (default)
```

---

## Development Notes
- All service functions return Pydantic schema objects for type safety.
- File upload endpoints use a two-step process: upload file, then create metadata record.
- CORS is enabled for `http://localhost:5173` (frontend dev).
- To add new models/routes, follow the modular structure in `models/`, `schemas/`, `services/`, and `routes/`.

---

## License
MIT (or project-specific) 