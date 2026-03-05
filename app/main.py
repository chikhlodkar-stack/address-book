import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.endpoints import addresses
from app.core.config import settings  # Import settings
from app.core.logging_config import (
    configure_logging,
)  # Import the logging config function

# Configure logging FIRST
configure_logging()
logger = logging.getLogger("app")  # Get a logger for our application

# Define the lifespan context manager
# Code before 'yield' runs at startup.
# Code after 'yield' runs at shutdown.
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    logger.info("Application starting up...")
    logger.info(f"Using database: {settings.DATABASE_URL}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    yield  # <-- This is where your application runs
    logger.info("Application shutting down...")

app = FastAPI(
    title="Address Book API",
    version="0.1.0",  # Added version from pyproject.toml
    description="A FastAPI application for managing an address book with geospatial querying.",
    openapi_url="/api/v1/openapi.json"
    if settings.ENVIRONMENT == "development"
    else None,  # Conditionally show docs
    lifespan=lifespan
)

# Include the router from the addresses module
app.include_router(addresses.router, prefix="/api/v1/addresses", tags=["Addresses"])



@app.get("/")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    logger.info("Root endpoint called.")  # Example of logging
    return {"message": "Welcome to the Address Book API!"}
