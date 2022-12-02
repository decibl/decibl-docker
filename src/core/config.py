# File that takes system variables and puts them into python variables
from enum import Enum
import os, sys, logging
from logging.handlers import TimedRotatingFileHandler
import datetime

class Config(Enum):
    # Logging
    LOGGING_LEVEL = logging.DEBUG
    # For logging format, do datetime + file location then message
    LOGGING_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
    LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    # make filename based on date
    LOGGING_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "log_{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))))
    LOGGING_ENCODING = "utf-8"

# set logging config
logging.basicConfig(filename=Config.LOGGING_FILENAME.value, encoding=Config.LOGGING_ENCODING.value, level=Config.LOGGING_LEVEL.value, format=Config.LOGGING_FORMAT.value, datefmt=Config.LOGGING_DATE_FORMAT.value)

logging.info("Loading config file")
logger = logging.getLogger("Rotating Time Log")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(Config.LOGGING_FILENAME.value,
                                    when="h",
                                    interval=1,)
logger.addHandler(handler)

# log a message that the config file has been loaded
logging.info("Loaded config file")