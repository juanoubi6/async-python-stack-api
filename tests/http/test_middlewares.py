import unittest

from fastapi.testclient import TestClient

from app import api

client = TestClient(api)


class TestMiddlewares(unittest.TestCase):

    def test_add_process_time_header_returns_header(self):
        response = client.get("/health")

        assert response.status_code == 200
        assert response.headers.get("X-Process-Time", None) is not None
