"""
Extensions for Entrypoint Layer.

This module provides utility functions to integrate FastAPI exception handlers with the application's
domain-specific exceptions. It ensures that custom errors in the domain layer are transformed into appropriate
HTTP responses when they propagate to the HTTP layer.

Note:
    For simpler requirements, use extension.py. For more complex needs, consider extensions/$package.py for better clarity and scalability.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models.exception import (
    PokemonAlreadyExists,
    PokemonError,
    PokemonNotFound,
    PokemonUnknownError,
)


def addExceptionHandler(app: FastAPI):
    @app.exception_handler(PokemonError)
    @app.exception_handler(PokemonUnknownError)
    async def handleGeneralPokemonError(_, exc):
        return JSONResponse(
            content={
                "code": 400,
                "description": {f"{type(exc).__name__}: {exc}"},
                "data": {},
            },
            status_code=400,
        )

    @app.exception_handler(PokemonNotFound)
    async def handlePokemonNotFoundError(_, exc):
        return JSONResponse(
            content={
                "code": 404,
                "description": {f"{type(exc).__name__}: {exc}"},
                "data": {},
            },
            status_code=404,
        )

    @app.exception_handler(PokemonAlreadyExists)
    async def handlePokemonAlreadyExistError(_, exc):
        return JSONResponse(
            content={
                "code": 409,
                "description": {f"{type(exc).__name__}: {exc}"},
                "data": {},
            },
            status_code=409,
        )
