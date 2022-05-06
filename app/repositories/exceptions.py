class DatabaseParseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DatabaseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
