import io
import json
from difflib import unified_diff

import yaml

from .config import Configuration
from .exceptions import InvalidTargetFile
from .logging import (
    get_logger,
    get_logger_list,
)
from .vcs import get_vcs
from .versioning import Version


logger = get_logger(False)
logger_list = get_logger_list()


class FileUpdater:
    def __init__(self, config: Configuration, current_version: Version, new_version: Version):
        self.paths = config.files()
        self.current_version = current_version
        self.new_version = new_version
        self.search = config.search
        self.context = {
            "current_version": current_version.serialize(),
            "new_version": new_version.serialize(),
        }
        self.search_for: str = config.search.format(**self.context)
        self.replace_with: str = config.replace.format(**self.context)

    def _validate(self):
        """
        Checks that all files listed in the config have matching text to replace
        """
        serialized_version = self.search.format(**self.context)
        for path in self.paths:
            if not self._contains(path):
                raise InvalidTargetFile(
                    f"Did not find '{self.current_version}' or '{serialized_version}' in file {path}"
                )

    def _contains(self, path):
        serialized_version = self.search.format(**self.context)
        with io.open(path, 'rb') as f:
            search_lines = serialized_version.splitlines()
            lookbehind = []

            for lineno, line in enumerate(f.readlines()):
                lookbehind.append(line.decode('utf-8').rstrip("\n"))

                if len(lookbehind) > len(search_lines):
                    lookbehind = lookbehind[1:]

                if (search_lines[0] in lookbehind[0] and
                   search_lines[-1] in lookbehind[-1] and
                   search_lines[1:-1] == lookbehind[1:-1]):
                    logger.info("Found '{}' in {} at line {}: {}".format(
                        serialized_version, path, lineno - (len(lookbehind) - 1), line.decode('utf-8').rstrip()))
                    return True
        return False

    def _replace(self, path, dry_run=False):
        with io.open(path, 'rb') as f:
            file_content_before = f.read().decode('utf-8')

        file_content_after = file_content_before.replace(self.search_for, self.replace_with)

        if file_content_before == file_content_after:
            # TODO expose this to be configurable
            file_content_after = file_content_before.replace(
                self.current_version.original,
                self.replace_with,
            )

        if file_content_before != file_content_after:
            logger.info("{} file {}:".format(
                "Would change" if dry_run else "Changing",
                path,
            ))
            logger.info("\n".join(list(unified_diff(
                file_content_before.splitlines(),
                file_content_after.splitlines(),
                lineterm="",
                fromfile="a/"+path,
                tofile="b/"+path
            ))))
        else:
            logger.info("{} file {}".format(
                "Would not change" if dry_run else "Not changing",
                path,
            ))

        if not dry_run:
            with io.open(path, 'wb') as f:
                f.write(file_content_after.encode('utf-8'))

    def replace(self, dry_run=False):
        if self._validate():
            for path in self.paths:
                    self._replace(path, dry_run)

    def __str__(self):
        return self.paths

    def __repr__(self):
        return '<bumpv.ConfiguredFile:{}>'.format(self.paths)


class BumpClient:
    def __init__(self, config: Configuration, verbose=0, show_list=False, allow_dirty=False):
        self.logger = get_logger(show_list, verbose)
        self.logger_list = get_logger_list()
        self.config = config
        self.vcs = get_vcs(allow_dirty)
        self.current_version = Version.from_config(config)
        self.new_version = None

    def bump(self, part, dry_run=False):
        self.new_version = self.current_version.bump(part)
        # do replace
        updater = FileUpdater(self.config, self.current_version, self.new_version)

        updater.replace(dry_run)

        if self.config.tag:
            # print(f"TAG: {self.new_version.get_tag()}")
            self.vcs.tag(self.new_version.get_tag())

        if self.config.commit:
            for path in self.config.files():
                self.vcs.add_path(path)
            message = self.config.message.format(
                current_version=self.current_version.serialize(),
                new_version=self.new_version.serialize(),
            )
            # print(f"COMMITTING: {message}")
            import ipdb; ipdb.set_trace()
            self.vcs.commit(message)
        return self.new_version

    def dict(self):
        return {
            "old_version": self.current_version.serialize(),
            "new_version": self.new_version.serialize(),
            "tag": self.new_version.get_tag(),
        }

    def json(self):
        return json.dumps(self.dict())

    def yaml(self):
        return yaml.dump(self.dict())
