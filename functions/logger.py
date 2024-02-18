import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def configure_logger():
    # Create a logs directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging to use TimedRotatingFileHandler
    log_filename = os.path.join(log_dir, 'app.log')
    handler = TimedRotatingFileHandler(log_filename, when='midnight', interval=1, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger()
    logger.addHandler(handler)
    
    return logger