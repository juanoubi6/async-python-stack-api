from fastapi import status
from fastapi.responses import JSONResponse

from app.builder import FastAPIWrapper, decorate_api, ErrorResponse
from app.domain import User, UserPrototype

api = FastAPIWrapper(default_response_class=JSONResponse)


@api.on_event("startup")
async def add_runtime_objects():
    await decorate_api(api)


@api.get(
    path="/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}}
)
async def get_user(user_id: int):
    return await api.user_service.get_user(user_id)


@api.post(
    path="/users",
    status_code=status.HTTP_201_CREATED,
    response_model=User
)
async def create_user(prototype: UserPrototype):
    return await api.user_service.create_user(prototype)
