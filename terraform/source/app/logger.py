from logging import getLogger, INFO, basicConfig, Logger

__format = "%(levelname)s - %(name)s [%(filename)s:%(lineno)d] >>> %(message)s"

def set_logger(logger_name: str) -> Logger:
    basicConfig(format=__format, level=INFO)
    return getLogger(logger_name)
