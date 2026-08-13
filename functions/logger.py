import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configure_logger(name: str = "anzeigen_app", level: int = logging.INFO):
    """Create and configure a single application logger.

    The app should use an explicit logger name instead of the root logger so
    repeated imports or reloads do not add duplicate file handlers.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    log_filename = os.path.join(log_dir, "app.log")
    file_handler = next(
        (handler for handler in logger.handlers if isinstance(handler, TimedRotatingFileHandler) and getattr(handler, "baseFilename", None) == log_filename),
        None,
    )

    if file_handler is None:
        file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=5)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(file_handler)

    stream_handler = next(
        (handler for handler in logger.handlers if isinstance(handler, logging.StreamHandler) and not isinstance(handler, TimedRotatingFileHandler)),
        None,
    )
    if stream_handler is None:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(stream_handler)

    return logger