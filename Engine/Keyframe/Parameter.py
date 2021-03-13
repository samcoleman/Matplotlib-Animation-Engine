from typing import List, Union
from Engine.Keyframe.Keyframe import KeyframeObject

class Parameter:
    def __init__(self, name: str, value):
        self._name = name
        self._value = value
        self.type = type(value)

    def get_name(self):
        return self._name

    def set_value(self, value):
        self._value = value
        self.type = type(value)

    def get_value(self):
        return self._value

"""
class RangeParameter(Parameter):
    def __init__(self, value=None, minimum=None, maximum=None):
        super(RangeParameter, self).__init__(value)
        self._min = minimum
        self._max = maximum

    # Could probs do some type checking here
    def set_min(self, minimum):
        if type(minimum) == self.type:
            self._min = minimum

    def get_min(self):
        return self._min

        # Could probs do some type checking here
    def set_max(self, maximum):
        if type(maximum) == self.type:
            self._max = maximum

    def get_max(self):
        return self._max
"""


class ParameterKeyframeObject(KeyframeObject):
    def __init__(self, parameter: Parameter):
        super(ParameterKeyframeObject, self).__init__()
        self._handle = parameter


class SetParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, value):
        super(SetParam, self).__init__(parameter)
        self._value = value

    def _update(self, adj_progress: float):
        self._handle.set_value(self._value)


class InterpParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, from_val=None, to_val=None):
        super(InterpParam, self).__init__(parameter)
        self._from_val = from_val
        self._to_val = to_val

    def _interp(self, p):
        print(p)
        if self._from_val is None or self._to_val is None:
            return self._handle.get_value()

        return self._from_val + (self._to_val - self._from_val) * p

    def _update(self, adj_progress: float):
        self._handle.set_value(self._interp(adj_progress))
