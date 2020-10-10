class SparkleError(Exception):
    def __init__(self, msg='Exception message not specified')
        self.msg= msg

    def __str__(self):
        return self.msg

class ConfigError(SparkleError):
    pass