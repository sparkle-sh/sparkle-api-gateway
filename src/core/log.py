import logging
import os

LOG_DIRECTORY = './logs/'

def get_logger(name: str) -> logging.Logger:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    root = logging.getLogger(name)

    formatter = logging.Formatter(log_format)
    root.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    if not os.path.isdir(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)

    file_handler = logging.FileHandler(LOG_DIRECTORY + "sparkle-api-gateway.log")

    root.propagate = False
    root.addHandler(file_handler)
    root.addHandler(console)
    return root
