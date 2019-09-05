import io
from difflib import unified_diff

from ..logging import get_logger


logger = get_logger(False)


class ConfiguredFile(object):
    def __init__(self, path, versionconfig):
        self.path = path
        self._versionconfig = versionconfig

    def should_contain_version(self, version, context):

        context['current_version'] = self._versionconfig.serialize(version, context)

        serialized_version = self._versionconfig.search.format(**context)

        if self.contains(serialized_version):
            return

        msg = "Did not find '{}' or '{}' in file {}".format(version.original, serialized_version, self.path)

        if version.original:
            assert self.contains(version.original), msg
            return

        assert False, msg

    def contains(self, search):
        with io.open(self.path, 'rb') as f:
            search_lines = search.splitlines()
            lookbehind = []

            for lineno, line in enumerate(f.readlines()):
                lookbehind.append(line.decode('utf-8').rstrip("\n"))

                if len(lookbehind) > len(search_lines):
                    lookbehind = lookbehind[1:]

                if (search_lines[0] in lookbehind[0] and
                   search_lines[-1] in lookbehind[-1] and
                   search_lines[1:-1] == lookbehind[1:-1]):
                    logger.info("Found '{}' in {} at line {}: {}".format(
                        search, self.path, lineno - (len(lookbehind) - 1), line.decode('utf-8').rstrip()))
                    return True
        return False

    def replace(self, current_version, new_version, context, dry_run):

        with io.open(self.path, 'rb') as f:
            file_content_before = f.read().decode('utf-8')

        context['current_version'] = self._versionconfig.serialize(current_version, context)
        context['new_version'] = self._versionconfig.serialize(new_version, context)

        search_for = self._versionconfig.search.format(**context)
        replace_with = self._versionconfig.replace.format(**context)

        file_content_after = file_content_before.replace(
            search_for, replace_with
        )

        if file_content_before == file_content_after:
            # TODO expose this to be configurable
            file_content_after = file_content_before.replace(
                current_version.original,
                replace_with,
            )

        if file_content_before != file_content_after:
            logger.info("{} file {}:".format(
                "Would change" if dry_run else "Changing",
                self.path,
            ))
            logger.info("\n".join(list(unified_diff(
                file_content_before.splitlines(),
                file_content_after.splitlines(),
                lineterm="",
                fromfile="a/"+self.path,
                tofile="b/"+self.path
            ))))
        else:
            logger.info("{} file {}".format(
                "Would not change" if dry_run else "Not changing",
                self.path,
            ))

        if not dry_run:
            with io.open(self.path, 'wb') as f:
                f.write(file_content_after.encode('utf-8'))

    def __str__(self):
        return self.path

    def __repr__(self):
        return '<bumpv.ConfiguredFile:{}>'.format(self.path)
