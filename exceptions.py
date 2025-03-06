from enum import Enum

class ServerError(Enum):
    pass


class ServerException(Exception):
    def __init__(self, 
                exception_data: ServerError = None,
                code: str = None,
                error: str = None,
                developer_message: str = None,
                *args):
        if exception_data:
            self.code = exception_data.code
            self.message = exception_data.message
            self.developer_message = exception_data.developer_message

        if code:
            self.code = code
        if error:
            self.message = error
        if developer_message:
            self.developer_message = developer_message

        super().__init__(*args)

class NotFoundException(ServerException):
    pass


class ValidationException(ServerException):
    pass