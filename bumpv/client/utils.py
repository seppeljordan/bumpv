import logging
import os
import sys
from argparse import _AppendAction
from datetime import datetime


_logger = None
_logger_list = None


def get_logger(show_list, verbose=0):
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

    if show_list:
        logger_list.setLevel(1)

    log_level = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }.get(verbose, logging.DEBUG)

    _logger.setLevel(log_level)
    return _logger


def get_logger_list():
    global _logger_list
    if _logger_list is None:
        _logger_list = logging.getLogger("bumpv.list")
    return _logger_list


def prefixed_environ():
    return dict((("${}".format(key), value) for key, value in os.environ.items()))


def time_context():
    return {
        'now': datetime.now(),
        'utcnow': datetime.utcnow(),
    }


def merge_dicts(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged


class DiscardDefaultIfSpecifiedAppendAction(_AppendAction):

    """
    Fixes bug http://bugs.python.org/issue16399 for 'append' action
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(self, "_discarded_default", None) is None:
            setattr(namespace, self.dest, [])
            self._discarded_default = True

        super(DiscardDefaultIfSpecifiedAppendAction, self).__call__(
                parser, namespace, values, option_string=None)
