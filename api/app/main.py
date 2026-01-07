from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import init_db
from .routes.clans import router as clans_router
from .config import get_settings

settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="Vertigo Games Clan API",
    description="REST API for managing game clans - Vertigo Games Data Engineer Case Study",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database tables on application startup."""
    init_db()


@app.get("/", tags=["health"])
def root():
    """Root endpoint with API information."""
    return JSONResponse(content={
        "message": "Vertigo Games Clan API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "create_clan": "POST /clans",
            "list_clans": "GET /clans",
            "search_clans": "GET /clans/search?name=xxx",
            "delete_clan": "DELETE /clans/{id}"
        }
    })


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy", "environment": settings.app_env}


# Include routers
app.include_router(clans_router)
