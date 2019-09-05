from .functions import NumericFunction


class PartConfiguration(object):
    function_cls = NumericFunction

    def __init__(self, *args, **kwds):
        self.function = self.function_cls(*args, **kwds)

    @property
    def first_value(self):
        return str(self.function.first_value)

    @property
    def optional_value(self):
        return str(self.function.optional_value)

    def bump(self, value=None):
        return self.function.bump(value)
