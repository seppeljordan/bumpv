import os
from configparser import ConfigParser

from .exceptions import InvalidConfigPath, OptionNotFound
from ..logging import get_logger


logger = get_logger()

FILE_SECTION_PREFIX = "bumpv:file:"
PART_SECTION_PREFIX = "bumpv:part:"


DEFAULT = {
    "bumpv": {
        "current_version": "",
        "commit": False,
        "tag": False,
        "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)",
        "serialize": "{major}.{minor}.{patch}",
        "search": "{current_version}",
        "replace": "{new_version}",
        "tag_name": "v{new_version}",
        "message": "Bump version: {current_version} → {new_version}",
    }
}


def new_config_file(name=".bumpv.cfg", initial_version="0.1.0"):
    DEFAULT["bumpv"]["current_version"] = initial_version
    config = ConfigParser()
    config.read_dict(DEFAULT)
    with open(name, "w") as conf_file:
        config.write(conf_file)


class Configuration:
    def __init__(self, file_path=".bumpv.cfg", *args, **kwargs):
        config = ConfigParser()
        config.read_dict(DEFAULT)
        if os.path.exists(file_path):
            config.read(file_path)
        else:
            raise InvalidConfigPath(f"no file found at: {file_path}")

        self._config = config
        self.file_path = file_path

        bumpv_section = self.get_section("bumpv")
        self.current_version = bumpv_section.get("current_version")
        self.commit = bumpv_section.getboolean("commit")
        self.tag = bumpv_section.getboolean("tag")
        self.tag_name = bumpv_section.get("tag_name")
        self.parse = bumpv_section.get("parse")
        self.serialize = bumpv_section.get("serialize").split("\n")
        self.search = bumpv_section.get("search")
        self.replace = bumpv_section.get("replace")
        self.message = bumpv_section.get("message")

    def __repr__(self):
        return f"<bumpv.Configuration: {self.file_path}>"

    @classmethod
    def new(cls, name=".bumpv.cfg", initial_version="0.1.0"):
        new_config_file(name, initial_version)
        return Configuration(file_path=name)

    def get_section(self, key):
        return self._config[key]

    def get_raw_section_option(self, key, option):
        try:
            return self._config[key].get(option, "")
        except KeyError:
            raise OptionNotFound(f"option '{option}'' not found in section '{key}'")

    def get_section_names(self, key):
        names = []
        for section in self._config.sections():
            if section == "bumpv":
                continue
            _, section, name = section.split(":")
            if section == key:
                names.append(name)
        return names

    def files(self):
        return self.get_section_names("file")

    def get_file_section(self, file_path):
        return self.get_section(f"{FILE_SECTION_PREFIX}{file_path}")

    def parts(self):
        return self.get_section_names("part")

    def get_part_section(self, part):
        return self.get_section(f"{FILE_SECTION_PREFIX}{part}")

    def set_value(self, key, option, value):
        self._config[key][option] = value

    def write(self, out=None):
        if out is None:
            out = self.file_path

        with open(out, "w") as conf_file:
            self._config.write(conf_file)
