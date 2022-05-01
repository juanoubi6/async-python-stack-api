import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime.date


# UserPrototype indicates all fields needed to create an user
class UserPrototype(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime.date
