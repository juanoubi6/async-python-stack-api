import os
from typing import Any

from fastapi import FastAPI

from app.config import AppConfig, get_config
from app.services import UserService


class FastAPIWrapper(FastAPI):
    def __init__(self, user_service: UserService = None, config: AppConfig = None, **extra: Any):
        super().__init__(**extra)
        self.config = config if config is not None else get_config(os.getenv("ENV", "local"))
        self.user_service = user_service
