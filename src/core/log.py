import logging


def get_logger(name: str) -> logging.Logger:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    root = logging.getLogger(name)

    formatter = logging.Formatter(log_format)
    root.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    root.addHandler(console)
    return root
