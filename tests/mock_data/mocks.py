import datetime

from app.domain import User, UserPrototype, Page, NEXT_PAGE_PREFIX, PageRequest

MOCK_USER = User(
    id=1,
    first_name="John",
    last_name="Doe",
    birth_date=datetime.date.today()
)

MOCK_USER_PROTOTYPE = UserPrototype(
    first_name="John",
    last_name="Doe",
    birth_date=datetime.date.today()
)


def create_mock_user_dto(user_id: int) -> dict:
    return {
        "id": user_id,
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": datetime.date.today()
    }


MOCK_EMPTY_PAGE = Page(
    data=[],
    next_page=NEXT_PAGE_PREFIX + "1",
    previous_page=None
)

MOCK_PAGE_REQUEST_WITHOUT_CURSOR = PageRequest(
    cursor=None,
    size=5
)
