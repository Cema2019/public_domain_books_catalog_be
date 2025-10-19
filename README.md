# 📚 Public Domain Library API

Live at [https://public-domain-books.onrender.com](https://public-domain-books.onrender.com)

A FastAPI-based REST API for searching public domain books, deployed on Render with a secure PostgreSQL database hosted on Aiven.io.

## ✨ Features

- **FastAPI-based REST API**: High-performance, asynchronous API for book searches.
- **ORM Integration**: SQLAlchemy with `psycopg2-binary` for robust database interactions.
- **Validation**: Pydantic for type-safe request and response handling.
- **CORS Support**: Enabled for integration with frontends (e.g., `sales-frontend`).
- **Health Check Endpoint**: Monitor API status.
- **Search Functionality**: Case-insensitive search by book title or author.
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (hosted on Aiven.io)
- **ORM / Driver**: SQLAlchemy (uses psycopg2-binary)
- **Validation**: Pydantic
- **Server**: Uvicorn
- **Deployment**: Render (Web Service with auto-scaling)
- **Dependencies**: See `requirements.txt`

## ⚙️ Requirements

- Python 3.10+
- PostgreSQL
- `pip` for installing dependencies

## 🔧 Setup

1. Clone the repository:

   ```
   git clone https://github.com/Cema2019/public_domain_books_catalog_be.git
   cd public_domain_books_catalog_be
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
   DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=verify-full&sslrootcert=/path/to/ca.pem
   CA_CERT_PATH=/path/to/ca.pem
   ```

5. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```
## 🚀 Deployment

The API is deployed on Render with the following configuration:
- **Platform**: Render Web Service with auto-scaling and zero-downtime deploys.
- **Database**: Aiven.io PostgreSQL with SSL (`sslmode=verify-full`) using a CA certificate stored in Render Secret Files (`/etc/secrets/ca.pem`).
- **Security**: Database credentials and CA certificate managed securely via Render Environment Variables and Secret Files.
- **Monitoring**: Logs available in Render Dashboard for debugging and performance tracking.

## 🛠️ Endpoints

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
  curl "https://public-domain-books.onrender.com/books?search=Hobbes" | python -m json.tool
  ```

## 🧭 API Documentation

FastAPI includes two auto-generated documentation UIs:

- **Swagger UI:** [https://public-domain-books.onrender.com/docs](https://public-domain-books.onrender.com/docs)
- **ReDoc:** [https://public-domain-books.onrender.com/redoc](https://public-domain-books.onrender.com/redoc)

## 🗃️ Database

- **Schema**: SQLAlchemy models define the books table.
- **Initialization**: `Base.metadata.create_all(bind=engine)` creates tables without overwriting existing data.
- **Security**: SSL connections (`sslmode=verify-full`) with Aiven.io’s CA certificate ensure secure database access.

## 📝 Notes

- Add `.env` to `.gitignore` to protect credentials.
- Use URL-encoded queries for multi-word search terms (e.g., `william%20shakespeare`).
- Logs can be viewed in the terminal during development or in Render’s dashboard for production.
