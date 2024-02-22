#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(funcName)s :: %(message)s')
path_to_logs = Path(__file__).cwd()
log_file = path_to_logs / 'logs/' / ("app_logger_" + datetime.today().strftime("%Y%m%d") + ".log")


def get_console_handler():
    """
    A function to create a console handler object.
    Outputs the information starting at INFO level to a console.
    Formats the output by using a pre-set format.
    :return: returns a console handler object
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # level=20
    console_handler.setFormatter(formatter)
    return console_handler


def get_file_handler():
    """
    Creates a file handler object that stores log outputs.
    :return: returns .logs file
    """
    file_handler = RotatingFileHandler(log_file)
    file_handler.setFormatter(formatter)
    return file_handler


def app_logger(logger_name):
    """
    A function to create a logger object with set parameters.
    The parameters are inherited from get_console_handler() function.
    Needs to be called in a file from where the exceptions will be logged.
    :param logger_name: Name for a logger.
           If "__name__" is passed, the logger will return the path to the file where the exception has occurred.
    :return: returns logger object
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    return logger
