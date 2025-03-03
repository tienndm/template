import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from entrypoints.http.extension import (
    addExceptionHandler as http_add_exception_handlers,
)
from entrypoints.http.pokemon.router import router as pokemon_http_router
from settings import APP_NAME, APP_VERSION
from settings.db import IS_RELATIONAL_DB, initializeDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    kwargs = {}

    if IS_RELATIONAL_DB:
        from repositories.relational_db.pokemon.orm import Base
        kwargs = {'declarativeBase': Base}

    await initializeDB(**kwargs)
    yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pokemon_http_router, tags=["HTTP"])
http_add_exception_handlers(app)


@app.exception_handler(Exception)
async def universalExceptionHandler(_, exc):
    return JSONResponse(
        content={"code": 500, "description": {"error": f"{type(exc).__name__}: {exc}"}, 'data': {}},
        status_code=500,
    )


@app.get("/", include_in_schema=False)
async def root():
    return JSONResponse(
        {
            "code": 200,
            "description": "success",
            "data": {"service": APP_NAME, "version": APP_VERSION},
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
