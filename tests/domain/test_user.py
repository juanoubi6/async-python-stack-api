import datetime
import unittest

from app.domain import User, UserPrototype


class TestUser(unittest.TestCase):

    def test_User_parsed_successfully(self):
        try:
            User(
                id=1,
                first_name="John",
                last_name="Doe",
                birth_date=datetime.date.today()
            )
        except Exception as ex:
            self.fail(f"failed to parse User: {ex}")

    def test_UserPrototype_parsed_successfully(self):
        try:
            UserPrototype(
                first_name="John",
                last_name="Doe",
                birth_date=datetime.date.today()
            )
        except Exception as ex:
            self.fail(f"failed to parse UserPrototype: {ex}")
