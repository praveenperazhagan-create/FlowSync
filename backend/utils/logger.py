"""
FlowSync Centralized Logging Utility
====================================
Configures formatted logging for backend modules, API routes, and AI services.
"""

import logging
import sys

def setup_logger(name: str = "flowsync") -> logging.Logger:
    """
    Creates and configures a standard logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
