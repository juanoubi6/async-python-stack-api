from typing import List, Any

from app.domain import PageRequest, PREVIOUS_PAGE_PREFIX, NEXT_PAGE_PREFIX


def calculate_data(page_request: PageRequest, data: List[Any]) -> List[Any]:
    if len(data) > page_request.size:
        if page_request.is_previous_cursor():
            return data[1:]
        if page_request.is_next_cursor() or page_request.cursor is None:
            return data[:-1]

    return data


def calculate_next_page_value(page_request: PageRequest, data_ids: List[str], data_size: int) -> str | None:
    if page_request.is_previous_cursor() or data_size > page_request.size:
        return NEXT_PAGE_PREFIX + data_ids[len(data_ids)-1]

    return None


def calculate_previous_page_value(page_request: PageRequest, data_ids: List[str], data_size:int) -> str | None:
    if page_request.cursor is None:
        return None

    if page_request.is_next_cursor() or data_size > page_request.size:
        return PREVIOUS_PAGE_PREFIX + data_ids[0]

    return None
