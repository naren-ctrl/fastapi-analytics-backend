from sqlalchemy import create_engine, Column, String, Integer, DateTime, Index
from sqlalchemy.orm import declarative_base, sessionmaker  # Updated import!
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import DATABASE_URL

# Create the base class for models
Base = declarative_base()

# Create database engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Event model/table
class Event(Base):
    __tablename__ = "events"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    path = Column(String)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)

# Create composite index for fast queries by site and date
Index('idx_site_timestamp', Event.site_id, Event.timestamp)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
