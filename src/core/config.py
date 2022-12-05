# File that takes system variables and puts them into python variables
import os, sys, logging
from logging.handlers import TimedRotatingFileHandler
import datetime

# ---------------------------------------------------------------------------------------------
#                                      Logging
# ---------------------------------------------------------------------------------------------

LOGGING_LEVEL = logging.INFO
# For logging format, do datetime + file location then message
LOGGING_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# make filename based on date
LOGGING_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "log_{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))))
LOGGING_ENCODING = "utf-8"

logging.info("Making folder for logs")
if not os.path.exists(os.path.dirname(LOGGING_FILENAME)):
    os.makedirs(os.path.dirname(LOGGING_FILENAME))


logging.basicConfig(filename=LOGGING_FILENAME, encoding=LOGGING_ENCODING, level=LOGGING_LEVEL, format=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)

logging.info("Loading config file")
logger = logging.getLogger("Rotating Time Log")
handler = TimedRotatingFileHandler(LOGGING_FILENAME,
                                    when="h",
                                    interval=1,)
logger.addHandler(handler)

# log a message that the config file has been loaded
logging.info("Loaded config file")

# make logging folder if it doesn't exist

# ---------------------------------------------------------------------------------------------
#                                      Database
# ---------------------------------------------------------------------------------------------

DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analyticsdb", "analytics.db"))

# make database folder if it doesn't exist
logging.info("Making folder for database")
if not os.path.exists(os.path.dirname(DATABASE_PATH)):
    os.makedirs(os.path.dirname(DATABASE_PATH))

# ---------------------------------------------------------------------------------------------
#                                      Sound Files
# ---------------------------------------------------------------------------------------------

# make sound folder if it doesn't exist
logging.info("Making folder for sound files")
SOUNDFILES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "soundfiles"))
if not os.path.exists(SOUNDFILES_PATH):
    os.makedirs(SOUNDFILES_PATH)
    

# ---------------------------------------------------------------------------------------------
#                                      Backups
# ---------------------------------------------------------------------------------------------

BACKUPS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups"))
DATABASE_BACKUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups", "database"))
LOGS_BACKUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups", "logs"))
# make backup folder if it doesn't exist
logging.info("Making folder for backups")
if not os.path.exists(BACKUPS_PATH):
    os.makedirs(BACKUPS_PATH)
if not os.path.exists(DATABASE_BACKUP_PATH):
    os.makedirs(DATABASE_BACKUP_PATH)
if not os.path.exists(LOGS_BACKUP_PATH):
    os.makedirs(LOGS_BACKUP_PATH)