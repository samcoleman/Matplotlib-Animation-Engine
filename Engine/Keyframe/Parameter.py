from typing import List, Union


class Parameter:
    def __init__(self, value=None, minimum=None, maximum=None):
        self._value = value
        self._min = minimum
        self._max = maximum
        self.type = None

        if type(value) is not None:
            self.type = type(value)
        if type(minimum) is not None:
            self.type = type(value)
        if type(maximum) is not None:
            self.type = type(value)

    # Could probs do some type checking here
    def set(self, value=None, minimum=None, maximum=None):
        if self._value is None:
            self._value = value

        if self._min is None:
            self._min = minimum

        if self._max is None:
            self._max = maximum

        if type(value) is not None:
            self.type = type(value)
        if type(minimum) is not None:
            self.type = type(value)
        if type(maximum) is not None:
            self.type = type(value)

    def interp(self, p):
        if self._min is None or self._max is None:
            return self._value

        self._value = self._min + (self._max - self._min) * p
        return self._value
