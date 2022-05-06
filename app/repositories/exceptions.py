from app.domain import AppException


class DatabaseParseException(AppException):
    pass


class DatabaseException(AppException):
    pass


class TransactionAlreadyStartedException(AppException):
    pass
