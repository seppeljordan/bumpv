import re

from .exceptions import (
    UnknownVersionPartError,
    VersionStringParseError,
)


def _parse(version_string: str, parse: str) -> dict:
    parse_regex = re.compile(parse, re.VERBOSE)
    match = parse_regex.search(version_string)
    if not match:
        raise VersionStringParseError(f"unable to parse version string '{version_string}' with pattern '{parse}'")
    return match.groupdict()


REPR_SERIALIZE_TEMPLATE = "major={major} minor={minor} patch={patch} release={release}"
TEMPLATE_VARIABLE_PATTERN = re.compile(r"{(\w+)}")


class Version:
    UnknownVersionPartError = UnknownVersionPartError
    VersionStringParseError = VersionStringParseError

    def __init__(self, major: int, minor: int, patch: int,
                 release: str = None, original=None, serialize_formats=None, tag_name="v{new_version}"):
        self._major = int(major)
        self._minor = int(minor)
        self._patch = int(patch)
        self._release = release
        self.tag_name = tag_name
        if original is None:
            self.original = self
        else:
            self.original = original

        if serialize_formats is None:
            self.serialize_formats = ["{major}.{minor}.{patch}"]

    @classmethod
    def from_config(cls, config):
        version_string = config.current_version
        parse = config.parse
        serialize_formats = config.serialize
        tag_name = config.tag_name

        match = _parse(version_string, parse)
        return Version(serialize_formats=serialize_formats, tag_name=tag_name, **match)

    @classmethod
    def from_version_string(cls, version_string, parse):
        match = _parse(version_string, parse)
        return Version(**match)

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise KeyError(err)

    def __iter__(self):
        return iter({
            "major": self._major,
            "minor": self._minor,
            "patch": self._patch,
            "release": self._release,
        })

    def _pattern_matches_values(self, pattern):
        vars = TEMPLATE_VARIABLE_PATTERN.findall(pattern)
        for var in vars:
            if getattr(self, var) is None:
                return False
        return True
    
    def __repr__(self):
        return f"<bumpv.Version: {self.serialize(REPR_SERIALIZE_TEMPLATE)}>"

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    @property
    def release(self):
        return self._release

    def serialize(self, patterns=None):
        if patterns is None:
            patterns = ["{major}.{minor}.{patch}"]

        for pattern in patterns:
            if self._pattern_matches_values(pattern):
                return pattern.format(**{
                    "major": self._major,
                    "minor": self._minor,
                    "patch": self._patch,
                    "release": self._release,
                })

    def bump_major(self):
        new_major = self._major + 1
        return Version(new_major, 0, 0, release=self._release)

    def bump_minor(self):
        new_minor = self._minor + 1
        return Version(self._major, new_minor, 0, release=self._release)

    def bump_patch(self):
        new_patch = self._patch + 1
        return Version(self._major, self._minor, new_patch, release=self._release)

    def bump_release(self):
        raise NotImplemented

    def bump(self, part_name):
        if part_name == "major":
            return self.bump_major()
        elif part_name == "minor":
            return self.bump_minor()
        elif part_name == "patch":
            return self.bump_patch()
        else:
            raise UnknownVersionPartError(part_name)

    def get_tag(self, tag_format=None, serialize_formats=None):
        if tag_format is None:
            tag_format = self.tag_name

        if serialize_formats is None:
            serialize_formats = self.serialize_formats

        tag_string = self.serialize(serialize_formats)
        return tag_format.format(new_version=tag_string)
