import os
import logging

from app.core.config import LOG_DIR,LOG_FILE


def configure_logging():    

    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join(LOG_DIR,LOG_FILE),
                    mode="a",
                    encoding="utf-8")
    stream_handler = logging.StreamHandler()


    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

