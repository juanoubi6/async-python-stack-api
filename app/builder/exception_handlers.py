from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.domain import DomainException, ResourceNotFoundException, AppException
from app.repositories import DatabaseException, DatabaseParseException


class ErrorResponse(BaseModel):
    message: str
    error: str
    type: str


def add_error_handlers(api: FastAPI):
    @api.exception_handler(DatabaseException)
    async def resource_not_found_handler(_: Request, exc: DatabaseException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=_create_content_response("There was an error on some database operation", exc)
        )

    @api.exception_handler(DatabaseParseException)
    async def resource_not_found_handler(_: Request, exc: DatabaseParseException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=_create_content_response("There was an error parsing a database object", exc)
        )

    @api.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(_: Request, exc: ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=_create_content_response("The resource you requested was not found", exc)
        )

    @api.exception_handler(DomainException)
    async def domain_handler(_: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=_create_content_response("There was a problem with your request", exc)
        )


def _create_content_response(message: str, ex: Exception) -> dict:
    if isinstance(ex, AppException):
        return ErrorResponse(
            message=message,
            error=ex.message,
            type=str(type(ex).__name__)
        ).dict()
    else:
        return ErrorResponse(
            message=message,
            error=str(ex),
            type=str(type(ex).__name__)
        ).dict()
