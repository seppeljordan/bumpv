import io
from difflib import unified_diff

from .exceptions import InvalidTargetFile
from ..logging import get_logger

from typing import TYPE_CHECKING
from ..config import Configuration
from ..versioning import Version


logger = get_logger()


class FileUpdater:
    def __init__(self, config: Configuration, current_version: Version, new_version: Version):
        self.config = config
        self.paths = config.files()
        self.current_version = current_version
        self.new_version = new_version
        self.context = {
            "current_version": current_version.serialize(),
            "new_version": new_version.serialize(),
        }

    def _validate(self):
        """
        Checks that all files listed in the config have matching text to replace
        """
        for path in self.paths:
            options = self.config.get_file_section(path)
            serialized_version = options["search"].format(**self.context)
            if not self._contains(path):
                raise InvalidTargetFile(
                    f"Did not find '{self.current_version}' or '{serialized_version}' in file {path}"
                )
        return True

    def _contains(self, path):
        try:
            with io.open(path, 'rb') as f:
                options = self.config.get_file_section(path)
                serialized_version = options["search"].format(**self.context)
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
        except FileNotFoundError:
            raise InvalidTargetFile(f"file listed in config not found: '{path}'")

    def _replace(self, path, dry_run=False):
        with io.open(path, 'rb') as f:
            file_content_before = f.read().decode('utf-8')

        options = self.config.get_file_section(path)
        search_for = options["search"].format(**self.context)
        replace_with = options["replace"].format(**self.context)

        file_content_after = file_content_before.replace(search_for, replace_with)

        if file_content_before == file_content_after:
            # TODO expose this to be configurable
            file_content_after = file_content_before.replace(
                self.current_version.original,
                replace_with,
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
