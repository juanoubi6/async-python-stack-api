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


class PageRequest(BaseModel):
    cursor: str | None
    size: int

    @validator('cursor')
    def validate_cursor(cls, v: str):
        if v is not None:
            if not str.startswith(v, PREVIOUS_PAGE_PREFIX) and not str.startswith(v, NEXT_PAGE_PREFIX):
                raise PaginationException('Invalid page value')

        return v

    def is_previous_cursor(self) -> bool:
        return self.cursor is not None and str.startswith(self.cursor, PREVIOUS_PAGE_PREFIX)

    def is_next_cursor(self) -> bool:
        return self.cursor is not None and str.startswith(self.cursor, NEXT_PAGE_PREFIX)

    def get_cursor_value(self) -> str | None:
        if self.cursor is None:
            return self.cursor

        return self.cursor.lstrip(PREVIOUS_PAGE_PREFIX).lstrip(NEXT_PAGE_PREFIX)
