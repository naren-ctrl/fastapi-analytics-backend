from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EventInput(BaseModel):
    """Model for incoming event data validation"""
    site_id: str = Field(..., description="Site identifier", min_length=1)
    event_type: str = Field(..., description="Type of event (e.g., page_view)", min_length=1)
    path: Optional[str] = Field(None, description="URL path visited")
    user_id: Optional[str] = Field(None, description="User identifier")
    timestamp: datetime = Field(..., description="Event timestamp in ISO format")

    class Config:
        json_schema_extra = {
            "example": {
                "site_id": "site-abc-123",
                "event_type": "page_view",
                "path": "/pricing",
                "user_id": "user-xyz-789",
                "timestamp": "2025-11-15T18:30:01Z"
            }
        }

class StatsResponse(BaseModel):
    """Model for stats API response"""
    site_id: str
    date: Optional[str]
    total_views: int
    unique_users: int
    top_paths: list

    class Config:
        json_schema_extra = {
            "example": {
                "site_id": "site-abc-123",
                "date": "2025-11-15",
                "total_views": 1500,
                "unique_users": 450,
                "top_paths": [
                    {"path": "/pricing", "views": 300},
                    {"path": "/features", "views": 250}
                ]
            }
        }
