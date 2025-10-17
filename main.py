from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os, logging
from database import SessionLocal, Base, engine
import crud, schemas

# ---------------- Config ---------------- #
load_dotenv()
ENV = os.getenv("ENV", "development")       # default dev if not set

app = FastAPI(title="Public domain library")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",        # local dev frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Logging ---------------- #
logging.basicConfig(level=logging.WARNING)
app_logger = logging.getLogger('library_catalog')

# ---------------- Startup Event ---------------- #
@app.on_event("startup")
def startup_event():
    # Creates missing tables; does NOT overwrite existing tables
    Base.metadata.create_all(bind=engine)

# ---------------- Health Check Endpoint ---------------- #
@app.get("/health")
async def health_check():
    return {"status": "up"}

# ---------------- DB ---------------- #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Libros Endpoints ---------------- #
@app.get("/books", response_model=list[schemas.BookSchema])
async def get_books(search: str = Query(None), db: Session = Depends(get_db)):
    return crud.get_books(db, search)

