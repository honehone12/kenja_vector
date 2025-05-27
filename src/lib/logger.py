import logging

__log = None

def log() -> logging.Logger:
    if __log is None:
        raise ValueError("logger is not initialized")
    return __log

def init_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    __log = logging.getLogger(name)
    return __log
