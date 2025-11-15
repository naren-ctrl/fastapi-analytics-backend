from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, distinct
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import EventInput, StatsResponse
from app.database import SessionLocal, Event, get_db

app = FastAPI(
    title="Analytics Backend API",
    description="High-speed analytics event ingestion system",
    version="1.0.0"
)

# Background task function to save event to database
def save_event_to_db(event_data: dict):
    """
    Background function that saves event to database.
    Runs after the API response is sent to client.
    """
    db = SessionLocal()
    try:
        # Create Event object from data
        db_event = Event(**event_data)
        db.add(db_event)
        db.commit()
        print(f"✅ Event saved: {event_data['site_id']} - {event_data['event_type']}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error saving event: {e}")
    finally:
        db.close()

# SERVICE 1: INGESTION API (SUPER FAST!)
@app.post("/event", status_code=202)
async def ingest_event(event: EventInput, background_tasks: BackgroundTasks):
    """
    Fast ingestion endpoint - accepts events and queues them for processing.
    
    Returns immediately without waiting for database write.
    """
    try:
        # Convert Pydantic model to dict for background task
        event_data = event.model_dump()
        
        # Add task to background queue
        background_tasks.add_task(save_event_to_db, event_data)
        
        # Return immediately (client doesn't wait!)
        return {
            "status": "success",
            "message": "Event queued for processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# SERVICE 2: REPORTING API
@app.get("/stats", response_model=StatsResponse)
async def get_stats(site_id: str, date: str = None, db: Session = Depends(get_db)):
    """
    Retrieve aggregated analytics for a site.
    
    Parameters:
    - site_id: Site identifier (required)
    - date: Date in YYYY-MM-DD format (optional)
    """
    try:
        # Start with base query
        query = db.query(Event).filter(Event.site_id == site_id)
        
        # Filter by date if provided
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(func.date(Event.timestamp) == target_date)
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid date format. Use YYYY-MM-DD"
                )
        
        # Calculate total views
        total_views = query.count()
        
        # Calculate unique users
        unique_users = query.with_entities(
            func.count(distinct(Event.user_id))
        ).scalar() or 0
        
        # Get top 10 paths by views
        top_paths_query = (
            query.with_entities(
                Event.path,
                func.count(Event.path).label('views')
            )
            .filter(Event.path.isnot(None))
            .group_by(Event.path)
            .order_by(func.count(Event.path).desc())
            .limit(10)
            .all()
        )
        
        # Format top paths
        top_paths = [
            {"path": path, "views": views} 
            for path, views in top_paths_query
        ]
        
        return StatsResponse(
            site_id=site_id,
            date=date,
            total_views=total_views,
            unique_users=unique_users,
            top_paths=top_paths
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Analytics Backend API is operational",
        "endpoints": {
            "ingestion": "/event (POST)",
            "reporting": "/stats (GET)"
        }
    }
