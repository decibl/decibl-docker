# File that takes system variables and puts them into python variables
from enum import Enum
import os, sys, logging

class Config(Enum):
    # Logging
    LOGGING_LEVEL = logging.DEBUG
    # For logging format, do datetime + file location then message
    LOGGING_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
    LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOGGING_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "example.log"))
    LOGGING_ENCODING = "utf-8"

# set logging config
logging.basicConfig(filename=Config.LOGGING_FILENAME.value, encoding=Config.LOGGING_ENCODING.value, level=Config.LOGGING_LEVEL.value, format=Config.LOGGING_FORMAT.value, datefmt=Config.LOGGING_DATE_FORMAT.value)

# log a message that the config file has been loaded
logging.info("Loaded config file")