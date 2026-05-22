import logging
import sys

def get_logger(
    name: str = "MCP_RuneScape",
    level: int = logging.DEBUG,
    fmt: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S"
) -> logging.Logger:
    
    logger = logging.getLogger(name=name)
    logger.setLevel(level=level)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level=level)
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        console_handler.setFormatter(fmt=formatter)
        logger.addHandler(console_handler)

    logger.propagate = False

    return logger