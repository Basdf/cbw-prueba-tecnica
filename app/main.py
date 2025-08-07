from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.routes.api import api_router
from app.configs.settings import settings
from app.configs.debugger import initialize_fastapi_server_debugger_if_needed
from app.configs.logging import get_logging

log = get_logging(__name__)


def create_app() -> FastAPI:
    initialize_fastapi_server_debugger_if_needed()
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        debug=settings.DEBUGGER,
        description=settings.DESCRIPTION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
