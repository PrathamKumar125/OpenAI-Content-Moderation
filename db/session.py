from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import get_settings
from utils.logging import logger

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db_connection():
    try:
        with engine.connect() as conn:
            logger.info("Successfully connected to the database")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise