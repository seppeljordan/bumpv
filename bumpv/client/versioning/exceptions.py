class UnknownVersionPartError(Exception):
    def __init__(self, part_name):
        self.message = f"part name must be one of: ['major', 'minor', 'patch'] got: {part_name}"


class VersionStringParseError(Exception):
    pass


class IncompleteVersionRepresentationException(Exception):
    def __init__(self, message):
        self.message = message


class MissingValueForSerializationException(Exception):
    def __init__(self, message):
        self.message = message
