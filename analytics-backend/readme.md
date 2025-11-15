# Analytics Backend API

A high-performance website analytics event ingestion system built with FastAPI. This backend service captures analytics events at high volume and provides aggregated reporting APIs.

##  Problem Statement

Build a backend service to:
- Capture website analytics events with extremely fast response times
- Handle high-volume ingestion requests without blocking
- Provide aggregated analytics reporting

**Assignment:** TJRA Retail (OPC) Private Limited - Internshala Full Stack Development  
**Time Limit:** 4 hours  
**Status:** ✅ Completed

##  Architecture

### System Design

**Service 1: Fast Ingestion API**
- Endpoint: `POST /event`
- Uses FastAPI's `BackgroundTasks` for asynchronous processing
- Returns immediately (202 Accepted) without waiting for database writes
- Processes events in the background

**Service 2: Reporting API**
- Endpoint: `GET /stats`
- Aggregates event data by site and optional date
- Returns total views, unique users, and top 10 paths

**Database:**
- SQLite for simplicity (production-ready schema)
- Indexed columns for fast querying (`site_id`, `timestamp`, `user_id`)
- Composite index on `(site_id, timestamp)` for optimal performance

### Why This Architecture?

**FastAPI BackgroundTasks** chosen for:
- ✅ Zero external dependencies (no Redis required)
- ✅ Perfect for single-server deployments
- ✅ Instant response times (~400ms)
- ✅ Simple, maintainable code
- ✅ Meets all performance requirements

##  Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Quick Start

1. **Clone the repository**

2. **Install dependencies**
        pip install -r requirements.txt

3. **Configure environment**


4. **Run the server**
        python -m uvicorn app.main:app --reload


5. **Access the API**
- API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`

##  API Documentation

### Interactive Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Endpoints

#### POST /event - Ingest Analytics Event

Accepts analytics events and queues them for background processing.

**Request:**
    curl -X POST http://localhost:8000/event
-H "Content-Type: application/json"
-d '{
"site_id": "site-abc-123",
"event_type": "page_view",
"path": "/pricing",
"user_id": "user-xyz-789",
"timestamp": "2025-11-15T18:30:01Z"
}'
**Response (202 Accepted):**
{
"status": "success",
"message": "Event queued for processing"
}



**Fields:**
- `site_id` (required): Site identifier
- `event_type` (required): Event type (e.g., "page_view")
- `path` (optional): URL path visited
- `user_id` (optional): User identifier
- `timestamp` (required): ISO 8601 datetime

#### GET /stats - Retrieve Analytics

Returns aggregated analytics data for a specific site.

**Request:**
curl "http://localhost:8000/stats?site_id=site-abc-123&date=2025-11-15"



**Parameters:**
- `site_id` (required): Site identifier
- `date` (optional): Filter by date (YYYY-MM-DD format)

**Response (200 OK):**
{
"site_id": "site-abc-123",
"date": "2025-11-15",
"total_views": 1500,
"unique_users": 450,
"top_paths": [
{"path": "/pricing", "views": 300},
{"path": "/features", "views": 250}
]
}


##  Testing

### Using Interactive Docs (Recommended)

1. Start the server: `python -m uvicorn app.main:app --reload`
2. Navigate to `http://localhost:8000/docs`
3. Click on any endpoint → "Try it out"
4. Enter test data and click "Execute"

### Using cURL

**Test ingestion:**
curl -X POST http://localhost:8000/event
-H "Content-Type: application/json"
-d '{"site_id":"site-test","event_type":"page_view","path":"/home","user_id":"user-123","timestamp":"2025-11-15T19:00:00Z"}'



**Test stats:**
curl "http://localhost:8000/stats?site_id=site-test"



## Project Structure

analytics-backend/
├── app/


│ ├── init.py # Package initializer



│ ├── config.py # Environment configuration


│ ├── database.py # Database models & connection


│ ├── models.py # Pydantic validation models


│ └── main.py # FastAPI app & endpoints


├── .gitignore # Git ignore rules


├── .env # Environment variables


├── requirements.txt # Python dependencies


└── README.md # This file



##  Tech Stack

- **Framework:** FastAPI 0.115.0
- **Server:** Uvicorn (ASGI)
- **Database:** SQLite with SQLAlchemy ORM
- **Validation:** Pydantic
- **Async Processing:** FastAPI BackgroundTasks

##  Design Decisions

1. **SQLite over PostgreSQL**: Quick setup, portable, identical schema makes PostgreSQL migration trivial

2. **BackgroundTasks over Redis**: Simpler architecture, no external dependencies, perfect for assignment scope

3. **Strategic Indexing**: Indexes on frequently queried columns ensure fast aggregations

4. **202 Status Code**: Indicates async processing, follows RESTful best practices

##  Performance

- **Ingestion Response Time:** ~400ms
- **Background Processing:** Non-blocking database writes
- **Concurrent Requests:** Handles high volume efficiently
- **Database Queries:** Optimized with composite indexes

##  Future Enhancements

- Redis for distributed deployments
- Authentication/API keys
- Rate limiting
- Batch event ingestion
- Additional metrics (bounce rate, session duration)
- Data retention policies
- PostgreSQL migration

##  Author


**[Narendar V]**  
