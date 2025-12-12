"""
API v1 Main Router
Kombiniert alle Endpunkt-Router.
"""
from fastapi import APIRouter
from .endpoints import entities, settings, logs, pending_rfids, system_settings

api_router = APIRouter()

# Entities Routes
api_router.include_router(
    entities.router,
    prefix="/entities",
    tags=["entities"]
)

# Settings Routes
api_router.include_router(
    settings.router,
    prefix="/settings",
    tags=["settings"]
)

# Logs Routes
api_router.include_router(
    logs.router,
    prefix="/logs",
    tags=["logs"]
)

# Pending RFIDs Routes
api_router.include_router(
    pending_rfids.router,
    prefix="/pending-rfids",
    tags=["pending-rfids"]
)

# System Settings Routes
api_router.include_router(
    system_settings.router,
    prefix="/system-settings",
    tags=["system-settings"]
)

