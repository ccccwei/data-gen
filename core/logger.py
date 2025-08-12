import logging
import sys
from typing import Optional

__all__ = ["setup_logger"]

def setup_logger(name: str = "data_gen", level: int = logging.INFO, fmt: Optional[str] = None):
    """Return a configured ``logging.Logger`` instance.

    Repeated calls with the same ``name`` will return the existing logger.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(level)
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(fmt or "[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger 