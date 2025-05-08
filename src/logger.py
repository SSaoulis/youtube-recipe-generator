import logging

logger = logging.getLogger("recipe_logger")
logger.propagate = False
if not logger.handlers:
    logger.addHandler(logging.NullHandler())
