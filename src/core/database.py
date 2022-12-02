import os, sys, logging

# add current file to system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# import config.py

import config

# log a message
logging.info("Loading database module")
