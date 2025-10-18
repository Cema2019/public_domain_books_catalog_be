# 📚 Public Domain Library API

A FastAPI backend for querying public domain books. Provides endpoints to fetch books and search by title or author.

## ✨ Features

- FastAPI-based REST API
- PostgreSQL database (via SQLAlchemy)
- CORS enabled for local frontend development
- Health check endpoint
- Search books by title or author (case-insensitive)

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (hosted on Aiven.io)
- **ORM / Driver**: SQLAlchemy (uses psycopg2-binary)
- **Validation**: Pydantic
- **Server**: Uvicorn
- **Dependencies**: See `requirements.txt`

## ⚙️ Requirements

- Python 3.10+
- PostgreSQL
- `pip` for installing dependencies

## 🔧 Setup

1. Clone the repository:

   ```
   git clone https://github.com/Cema2019/public_domain_books_catalog_be.git
   cd <repo-folder>
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   .\venv\Scripts\activate   # Windows (PowerShell)
   source venv/bin/activate       # Linux / Mac
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Configure your `.env` file with PostgreSQL credentials:

   ```
   ENV=development
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

5. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

## 🚀 Endpoints

### 💓 Health Check

- **GET** `/health`  
  Returns:
  ```json
  {
    "status": "up"
  }
  ```

### 📘 Get Books

- **GET** `/books?search=<term>`  
  Query books by title or author (case-insensitive).  
  Example:
  ```
  curl "http://127.0.0.1:8000/books?search=Hobbes" | python -m json.tool
  ```

## 🧭 API Documentation

FastAPI includes two auto-generated documentation UIs:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🗃️ Database

- SQLAlchemy models are used to define the `books` table.
- `Base.metadata.create_all(bind=engine)` will create missing tables without overwriting existing data.

## 📝 Notes

- Add `.env` to `.gitignore` to protect credentials.
- Use URL-encoded queries for multi-word search terms (e.g., `william%20shakespeare`).
- Logs can be viewed in the terminal during development or in Render’s dashboard for production.
