from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os, logging
from database import SessionLocal, Base, engine
import crud, schemas
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

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

# ---------------- Logging: show only Uvicorn logs, catch ping errors ---------------- #
logging.basicConfig(level=logging.WARNING)
app_logger = logging.getLogger('library_catalog')
logging.getLogger('apscheduler').setLevel(logging.CRITICAL)  # Hide APScheduler logs
logging.getLogger('httpx').setLevel(logging.CRITICAL)  # Hide httpx logs

# ---------------- Self-Ping Scheduler ---------------- #
scheduler = AsyncIOScheduler()  # Global scheduler instance

async def ping_self():
    """Send an internal GET request to /health to keep Render app awake."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://public-domain-books-catalog-be.onrender.com/health")
            if response.status_code != 200:
                app_logger.error(f"Self-ping failed with status {response.status_code}")
        except Exception as e:
            app_logger.error(f"Self-ping error: {str(e)}")

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(ping_self())
    scheduler.add_job(
        ping_self,
        trigger=IntervalTrigger(minutes=10),
        id="self_ping",
        max_instances=1,
        replace_existing=True
    )
    scheduler.start()

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

