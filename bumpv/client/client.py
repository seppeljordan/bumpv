from .utils import (
    get_logger,
    get_logger_list,
)
from .vcs import get_vcs

logger = get_logger(False)
logger_list = get_logger_list()


DEFAULTS = {
    "tag": False,
    "tag_name": "v{new_version}",
    "commit": False,
    "message": "Bump version: {current_version} → {new_version}"
}


class BumpClient:
    def __init__(self, config, verbose=0, show_list=False, allow_dirty=False):
        self.logger = get_logger(show_list, verbose)
        self.logger_list = get_logger_list()
        self.config = config
        self.vcs = get_vcs(allow_dirty)

    def bump(self, part, current_version=""):
        pass

    def json(self):
        pass

    def yaml(self):
        pass
