from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference

from app.adapters.routes.api import api_router
from app.configs.debugger import initialize_fastapi_server_debugger_if_needed
from app.configs.logging import get_logging
from app.configs.settings import settings
from app.domains.models.errors import DatabaseError, NotFoundError, WorkerError

log = get_logging(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.adapters.repositories.mongo.task import TaskMongoRepository
    from app.adapters.repositories.workers.task import TaskCeleryWorker
    from app.configs.mongo import MongoDBConfig
    from app.configs.settings import settings
    from app.domains.services.task import TaskService

    mongo_db = MongoDBConfig(uri=settings.MONGO_URI, db_name=settings.MONGO_DB_NAME)
    app.state.mongo_db = mongo_db
    app.state.task_service = TaskService(
        TaskMongoRepository(mongo_db=mongo_db), TaskCeleryWorker()
    )
    try:
        yield
    finally:
        await mongo_db.close_connection()


def create_app() -> FastAPI:
    initialize_fastapi_server_debugger_if_needed()
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        debug=settings.DEBUGGER,
        description=settings.DESCRIPTION,
        lifespan=lifespan,
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


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc: NotFoundError):
    log.error(
        f"NotFoundError: {exc.message}. Request data: method={request.method}, url={request.url}, headers={dict(request.headers)}"
    )
    try:
        body = await request.body()
        log.error(f"Request body: {body}")
    except Exception as e:
        log.error(f"Error reading request body: {e}")
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc: DatabaseError):
    log.error(
        f"DatabaseError: {exc.message}. Request data: method={request.method}, url={request.url}, headers={dict(request.headers)}"
    )
    try:
        body = await request.body()
        log.error(f"Request body: {body}")
    except Exception as e:
        log.error(f"Error reading request body: {e}")
    return JSONResponse(status_code=500, content={"detail": exc.message})


@app.exception_handler(WorkerError)
async def worker_error_handler(request, exc: WorkerError):
    log.error(
        f"WorkerError: {exc.message}. Request data: method={request.method}, url={request.url}, headers={dict(request.headers)}"
    )
    try:
        body = await request.body()
        log.error(f"Request body: {body}")
    except Exception as e:
        log.error(f"Error reading request body: {e}")
    return JSONResponse(status_code=500, content={"detail": exc.message})
