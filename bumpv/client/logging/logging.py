import logging
import os
import sys
from argparse import _AppendAction
from datetime import datetime


_logger = None
_logger_list = None


def get_logger(level: int = 0):
    global _logger
    logger_list = get_logger_list()
    if _logger is None:
        _logger = logging.getLogger("bumpv.logger")
    log_formatter = logging.Formatter('%(message)s')

    if len(_logger.handlers) == 0:
        ch = logging.StreamHandler(sys.stderr)
        ch.setFormatter(log_formatter)
        _logger.addHandler(ch)

    if len(logger_list.handlers) == 0:
        ch2 = logging.StreamHandler(sys.stdout)
        ch2.setFormatter(log_formatter)
        logger_list.addHandler(ch2)

    log_level = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }.get(level, logging.DEBUG)

    _logger.setLevel(log_level)
    return _logger


def get_logger_list():
    global _logger_list
    if _logger_list is None:
        _logger_list = logging.getLogger("bumpv.list")
    return _logger_list
