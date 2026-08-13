import logging
import socket

from app import get_available_port
from functions.logger import configure_logger


def test_configure_logger_does_not_duplicate_handlers():
    logger = configure_logger()
    first_count = len(logger.handlers)

    logger = configure_logger()
    second_count = len(logger.handlers)

    assert first_count == second_count
    assert logger.name == "anzeigen_app"
    assert logger.level == logging.INFO


def test_get_available_port_returns_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        preferred_port = sock.getsockname()[1]

    assert get_available_port(preferred_port) == preferred_port
