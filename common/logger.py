# coding=utf-8
"""
@Ref   : https://www.toptal.com/python/in-depth-python-logging
"""


import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_PATH = None
LOG_FILE = None


def init_log(log_path):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    global LOG_PATH
    LOG_PATH = log_path


def init_default_log_path():
    global LOG_PATH
    LOG_PATH = os.path.join(".", "log")


def get_log_file():
    # root_path = os.path.dirname(os.path.dirname(__file__))  # get the root path of project
    # log_path = os.path.join(LOG_PATH, 'log')
    if not LOG_PATH:
        init_default_log_path()
    log_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(LOG_PATH, '.'.join([log_name, 'log']))


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    global LOG_FILE
    LOG_FILE = get_log_file()
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False

    return logger
