import os
from configparser import ConfigParser, NoOptionError

from .exceptions import InvalidConfigPath
from ..logging import get_logger


logger = get_logger(False)

FILE_SECTION_PREFIX = "bumpv:file:"
PART_SECTION_PREFIX = "bumpv:part:"


DEFAULT = {
    "bumpv": {
        "current_version": "",
        "commit": False,
        "tag": False,
        "parse": r"(?P<_major>\d+)\.(?P<_minor>\d+)\.(?P<_patch>\d+)",
        "serialize": "{major}.{minor}.{patch}",
        "search": "{current_version}",
        "replace": "{new_version}",
        "tag_name": "v{new_version}"
    }
}


class Configuration:
    def __init__(self, file_path=".bumpv.cfg", *args, **kwargs):
        config = ConfigParser()
        config.read_dict(DEFAULT)
        if os.path.exists(file_path):
            config.read(file_path)
        else:
            raise InvalidConfigPath(f"no file found at: {file_path}")

        self._config = config

        self.current_version = ""
        self.commit = False
        self.tag = False
        self.parse = r"(?P<_major>\d+)\.(?P<_minor>\d+)\.(?P<_patch>\d+)"
        self.serialize = "v{major}.{minor}.{patch}"
        self.search = "{current_version}"
        self.replace = "{new_version}"

    def get_section_names(self, key):
        for section in self._config.sections():
            if section == "bumpv":
                continue
            _, section, name = section.split(":")
            if section == key:
                yield name

    def files(self):
        return self.get_section_names("file")

    def get_file_section(self, file_path):
        return self._config[f"{FILE_SECTION_PREFIX}{file_path}"]

    def parts(self):
        return self.get_section_names("part")

    def get_part_section(self, part):
        return self._config[f"{FILE_SECTION_PREFIX}{part}"]
