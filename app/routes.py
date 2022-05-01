import asyncio

from fastapi import status

from app.builder import build_api
from app.domain import User, UserPrototype

api = asyncio.run(build_api())


@api.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: int):
    return await api.user_service.get_user(user_id)


@api.post("/users", status_code=status.HTTP_200_OK, response_model=User)
async def create_user(prototype: UserPrototype):
    return await api.user_service.create_user(prototype)
