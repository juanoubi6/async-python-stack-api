from unittest.mock import patch, AsyncMock

import pytest

from app.domain import ResourceNotFoundException
from app.services import UserService
from tests.mock_data.mocks import MOCK_USER, MOCK_USER_PROTOTYPE

user_service = UserService(user_repository=AsyncMock())


@pytest.mark.asyncio
class TestUserService:

    @patch.object(user_service, "user_repository")
    async def test_get_user_returns_user_on_success(self, mock_user_repository):
        mock_user_repository.get_user = AsyncMock(return_value=MOCK_USER)

        response = await user_service.get_user(1)

        assert response == MOCK_USER

        mock_user_repository.get_user.assert_called_once_with(1)

    @patch.object(user_service, "user_repository")
    async def test_get_user_raises_ResourceNotFoundException_if_user_is_not_found(self, mock_user_repository):
        mock_user_repository.get_user = AsyncMock(return_value=None)

        with pytest.raises(ResourceNotFoundException):
            await user_service.get_user(1)

        mock_user_repository.get_user.assert_called_once_with(1)

    @patch.object(user_service, "user_repository")
    async def test_create_user_returns_user_on_success(self, mock_user_repository):
        mock_user_repository.create_user = AsyncMock(return_value=MOCK_USER)

        response = await user_service.create_user(MOCK_USER_PROTOTYPE)

        assert response == MOCK_USER

        mock_user_repository.start_tx.assert_called_once()
        mock_user_repository.create_user.assert_called_once_with(MOCK_USER_PROTOTYPE)
        mock_user_repository.commit_tx.assert_called_once()
