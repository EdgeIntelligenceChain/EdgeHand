

class BaseException(Exception):
    def __init__(self, msg):
        self.msg = msg
class TxnValidationError(BaseException):
    pass

class PortGenerateError(BaseException):
    pass

class Parse2MessageError(BaseException):
    pass

class ListenError(BaseException):
    pass

class UnwantedResultError(BaseException):
    pass


