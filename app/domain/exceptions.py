class AppException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DomainException(AppException):
    pass


class ResourceNotFoundException(AppException):
    pass


class PaginationException(AppException):
    pass
