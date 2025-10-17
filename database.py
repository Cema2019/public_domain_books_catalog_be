import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env variables (for local development)
load_dotenv()

# Database URL (set in .env locally, Render dashboard in production)
DATABASE_URL = os.getenv("DATABASE_URL")

# Path to CA cert (local .env overrides, Render defaults to /etc/secrets/ca.pem)
CA_CERT_PATH = os.getenv("CA_CERT_PATH", "/etc/secrets/ca.pem")

# SQLAlchemy engine with SSL for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Logs SQL queries (disable in production for speed)
    pool_pre_ping=True,  # Ensures dead connections are recycled
    connect_args={
        "sslmode": "verify-full",
        "sslrootcert": CA_CERT_PATH
    }
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for all models
Base = declarative_base()

# Import models so tables are registered
import models  # noqa
