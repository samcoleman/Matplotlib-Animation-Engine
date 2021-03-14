from Engine.Keyframe.Keyframe import KeyframeObject
from typing import Dict


class Parameter:
    def __init__(self, value):
        self._value = value
        self.type = type(value)

    def set_value(self, value):
        self._value = value
        self.type = type(value)

    def get_value(self):
        return self._value


class GlobalParameterManager:
    def __init__(self):
        self._parameters: Dict[str, Parameter] = dict()

    def attach_parameter(self, global_key: str, param: Parameter):
        self._parameters[global_key] = param

    def get_parameter(self, global_key: str):
        return self._parameters[global_key]

    # As Parameter is mutable, both keys will point to the same Parameter object
    def merge_parameters(self, key_kept: str, key_overwrite: str):
        self._parameters[key_overwrite] = self._parameters[key_kept]


class ParameterKeyframeObject(KeyframeObject):
    def __init__(self, parameter: Parameter):
        super(ParameterKeyframeObject, self).__init__()
        self._handle = parameter
        self._initial_value = parameter.get_value()

    # Update initial value which what the parameter is originally, repeated incase the value has changed
    #def _set_start(self):
    #    self._initial_value = self._handle.get_value()

    def reset(self):
        self._handle.set_value(self._initial_value)


class SetParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, value):
        super(SetParam, self).__init__(parameter)
        self._value = value

    def _update(self, adj_progress: float, duration: float):
        self._handle.set_value(self._value)


class InterpParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, from_val=None, to_val=None):
        super(InterpParam, self).__init__(parameter)
        self._from_val = from_val
        self._to_val = to_val

    def _interp(self, p):
        if self._from_val is None or self._to_val is None:
            return self._handle.get_value()

        return self._from_val + (self._to_val - self._from_val) * p

    def _update(self, adj_progress: float, duration: float):
        self._handle.set_value(self._interp(adj_progress))
