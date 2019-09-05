class UnknownVersionPartError(Exception):
    def __init__(self, part_name):
        self.message = f"part name must be one of: ['major', 'minor', 'patch'] got: {part_name}"


class Version:
    UnknownVersionPartError = UnknownVersionPartError

    def __init__(self, major: int, minor: int, patch: int, release: str = None, original=None):
        self._major = major
        self._minor = minor
        self._patch = patch
        self._release = release
        self.original = original

    @classmethod
    def from_config(cls, config):
        pass

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise KeyError(err)

    def __len__(self):
        return 3

    def __iter__(self):
        return iter({
            "major": self._major,
            "minor": self._minor,
            "patch": self._patch,
        })

    def __repr__(self):
        return f"<bumpv.Version:{self._major}.{self._minor}.{self._patch}>"

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

    def bump_major(self):
        new_major = self._major + 1
        return Version(new_major, 0, 0)

    def bump_minor(self):
        new_minor = self._minor + 1
        return Version(self._major, new_minor, 0)

    def bump_patch(self):
        new_patch = self._patch + 1
        return Version(self._major, self._minor, new_patch)

    def bump(self, part_name):
        if part_name == "major":
            return self.bump_major()
        elif part_name == "minor":
            return self.bump_minor()
        elif part_name == "patch":
            return self.bump_patch()
        else:
            raise UnknownVersionPartError(part_name)
