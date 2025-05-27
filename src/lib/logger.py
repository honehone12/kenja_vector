import logging

__log = None

def log() -> logging.Logger:
    global __log

    if __log is None:
        raise ValueError("logger is not initialized")
    return __log

def loginit(name: str) -> logging.Logger:
    global __log

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    __log = logging.getLogger(name)
    return __log
