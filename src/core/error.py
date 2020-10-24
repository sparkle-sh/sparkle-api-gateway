import enum


class ErrorCode(enum.IntEnum):
    INVALID_REQUEST = 1,
    CORRUPTED_PAYLOAD = 2,
    INVALID_CONFIG = 3,
    DATABASE_ERROR = 100 


class SparkleFatalError(Exception):
    def __init__(self, code: ErrorCode, description, name="SparkleFatalError"):
        super().__init__()
        self.code = code
        self.description = description
        self.name = name

    def __str__(self):
        return '<{}-{}/{}>'.format(self.name, self.code, self.description)


class SparkleError(SparkleFatalError):
    def __init__(self, code: ErrorCode, description, name="SparkleError"):
        super().__init__(code, description, name)


class ConfigError(SparkleError):
    def __init__(self, msg):
        super().__init__(ErrorCode.INVALID_CONFIG, msg, name="SparkleConfigError")    


class DatabaseError(SparkleError):
    def __init__(self, msg):
        super().__init__(ErrorCode.DATABASE_ERROR, msg, name="DatabaseError")