import datetime

from app.domain import User, UserPrototype

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
