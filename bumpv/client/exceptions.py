class IncompleteVersionRepresenationException(Exception):
    def __init__(self, message):
        self.message = message


class MissingValueForSerializationException(Exception):
    def __init__(self, message):
        self.message = message


class WorkingDirectoryIsDirtyException(Exception):
    def __init__(self, message):
        self.message = message
