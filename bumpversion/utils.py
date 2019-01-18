import logging


def get_logger():
    return logging.getLogger("bumpversion.logger")


def get_logger_list():
    return logging.getLogger("bumpversion.list")


def kv_string(d):
    return ", ".join("{}={}".format(k, v) for k, v in sorted(d.items()))


def merge_dicts(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged
