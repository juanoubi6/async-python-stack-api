from typing import List, TypeVar, Generic

from pydantic import BaseModel, validator

from app.domain.exceptions import PaginationException

PREVIOUS_PAGE_PREFIX = "PREV___"
NEXT_PAGE_PREFIX = "NEXT___"

T = TypeVar('T')


class Page(BaseModel, Generic[T]):
    data: List[T]
    next_page: str | None
    previous_page: str | None

    @validator('next_page')
    def validate_next_page(cls, v: str):
        if v is not None and not next_cursor_condition(v):
            raise PaginationException('Invalid next_page value')

        return v

    @validator('previous_page')
    def validate_previous_page(cls, v: str):
        if v is not None and not previous_cursor_condition(v):
            raise PaginationException('Invalid previous_page value')

        return v


class PageRequest(BaseModel):
    cursor: str | None
    size: int

    @validator('cursor')
    def validate_cursor(cls, v: str):
        return validate_cursor(v)

    def is_previous_cursor(self) -> bool:
        return previous_cursor_condition(self.cursor)

    def is_next_cursor(self) -> bool:
        return next_cursor_condition(self.cursor)

    def get_cursor_value(self) -> str | None:
        if self.cursor is None:
            return self.cursor

        return self.cursor.lstrip(PREVIOUS_PAGE_PREFIX).lstrip(NEXT_PAGE_PREFIX)


def previous_cursor_condition(value: str | None) -> bool:
    return value is not None and str.startswith(value, PREVIOUS_PAGE_PREFIX)


def next_cursor_condition(value: str | None) -> bool:
    return value is not None and str.startswith(value, NEXT_PAGE_PREFIX)


def validate_cursor(value: str) -> str | None:
    if value is not None:
        if not previous_cursor_condition(value) and not next_cursor_condition(value):
            raise PaginationException('Invalid page value')

    return value
