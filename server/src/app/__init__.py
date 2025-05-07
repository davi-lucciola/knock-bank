from fastapi import FastAPI
from typing import Callable
from contextlib import asynccontextmanager

from app import routes
from core.config import settings


@asynccontextmanager
async def default_lifespan(app: FastAPI):
    """Initialize application services."""
    # Process Like Consumers and CronJobs
    yield
    # Finishing that Process


def create_app(lifespan: Callable = default_lifespan) -> FastAPI:
    """Creating FastAPI application."""
    app = FastAPI(
        title=settings.API_TITLE, 
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL, 
        lifespan=lifespan
    )

    routes.init_routes(app)
    routes.add_exception_handlers(app)

    return app
