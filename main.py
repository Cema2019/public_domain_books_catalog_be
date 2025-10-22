from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os, logging, asyncio, httpx
from database import SessionLocal, Base, engine
import crud, schemas
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Base Page and the customization tools
from fastapi_pagination import Page as BasePage, add_pagination
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi_pagination.ext.sqlalchemy import paginate

# Re-define "Page" with our new explicit defaults.
Page = CustomizedPage[
    BasePage,
    UseParamsFields(
        size=Query(20, ge=1, description="Page size"), # Default size is 20
        page=Query(1, ge=1, description="Page number"), # Default page is 1
    ),
]

# ---------------- Config ---------------- #
load_dotenv()
ENV = os.getenv("ENV", "development")       # default dev if not set

app = FastAPI(title="Public domain library")

# -------- CORS middleware -------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",        # local dev frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Initialize pagination globally -------- #
add_pagination(app)

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

# ---------------- Books Endpoint ---------------- #
@app.get("/books", response_model=Page[schemas.BookSchema]) 
async def get_books(
    search: str | None = Query(None, description="Search by title or author"),
    db: Session = Depends(get_db)
):
    """
    Fetch paginated books — 20 results per page by default.
    Use ?page=2 for next results.
    """
    # 1. Build the query (doesn't need the db session)
    stmt = crud.get_books_query(search)
    
    # 2. Execute the query (this needs the db session)
    return paginate(db, stmt)


