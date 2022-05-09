import unittest

import pytest

from app.domain import PREVIOUS_PAGE_PREFIX, PageRequest, NEXT_PAGE_PREFIX, Page
from app.domain.exceptions import PaginationException


class TestPagination(unittest.TestCase):

    def test_Page_parsed_successfully(self):
        try:
            Page(
                data=[],
                next_page=NEXT_PAGE_PREFIX + "1",
                previous_page=PREVIOUS_PAGE_PREFIX + "1"
            )
        except Exception as ex:
            self.fail(f"failed to parse PageRequest: {ex}")

    def test_Page_throws_exception_for_invalid_next_page_value(self):
        with pytest.raises(PaginationException):
            Page(
                data=[],
                next_page=PREVIOUS_PAGE_PREFIX + "1",
                previous_page=None
            )

    def test_Page_throws_exception_for_invalid_previous_page_value(self):
        with pytest.raises(PaginationException):
            Page(
                data=[],
                next_page=None,
                previous_page=NEXT_PAGE_PREFIX + "1"
            )

    def test_PageRequest_parsed_successfully(self):
        try:
            PageRequest(cursor=PREVIOUS_PAGE_PREFIX + "1", size=5)
        except Exception as ex:
            self.fail(f"failed to parse PageRequest: {ex}")

    def test_PageRequest_throws_exception_for_invalid_cursor_value(self):
        with pytest.raises(PaginationException):
            PageRequest(cursor="value", size=5)

    def test_PageRequest_is_previous_cursor_returns_true_on_valid_cursor(self):
        valid_page_req = PageRequest(cursor=PREVIOUS_PAGE_PREFIX + "1", size=5)
        not_valid_page_req = PageRequest(cursor=None, size=5)

        assert valid_page_req.is_previous_cursor() is True
        assert not_valid_page_req.is_previous_cursor() is False

    def test_PageRequest_is_next_cursor_returns_true_on_valid_cursor(self):
        valid_page_req = PageRequest(cursor=NEXT_PAGE_PREFIX + "1", size=5)
        not_valid_page_req = PageRequest(cursor=None, size=5)

        assert valid_page_req.is_next_cursor() is True
        assert not_valid_page_req.is_next_cursor() is False

    def test_PageRequest_get_cursor_value_returns_str_value_for_valid_cursor(self):
        next_cursor_page_req = PageRequest(cursor=NEXT_PAGE_PREFIX + "1", size=5)
        previous_cursor_page_req = PageRequest(cursor=PREVIOUS_PAGE_PREFIX + "2", size=5)
        page_req_without_cursor = PageRequest(cursor=None, size=5)

        assert next_cursor_page_req.get_cursor_value() == "1"
        assert previous_cursor_page_req.get_cursor_value() == "2"
        assert page_req_without_cursor.get_cursor_value() is None
