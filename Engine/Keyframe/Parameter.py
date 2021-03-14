from Engine.Keyframe.Keyframe import KeyframeObject
from typing import Dict


class Parameter:
    def __init__(self, value: any) -> None:
        self._value = value
        self.type = type(value)

    # Type checking?
    def set_value(self, value: any) -> None:
        self._value = value
        self.type = type(value)

    def get_value(self) -> any:
        return self._value


# This can be used by the browse window for interactive parameter adjustment
class GlobalParameterManager:
    def __init__(self) -> None:
        self._global_parameters: Dict[str, Dict[str, Parameter]] = dict()

    def attach_local_parameters(self, instance_name: str, param: Dict[str, Parameter]) -> None:
        self._global_parameters[instance_name] = param

    def get_parameter(self, instance_name: str, local_key: str) -> Parameter:
        return self._global_parameters[instance_name][local_key]


class ParameterKeyframeObject(KeyframeObject):
    def __init__(self, parameter: Parameter) -> None:
        super(ParameterKeyframeObject, self).__init__()
        self._handle = parameter
        self._initial_value = parameter.get_value()

    # Update initial value which what the parameter is originally, repeated incase the value has changed
    #def _set_start(self):
    #    self._initial_value = self._handle.get_value()

    def reset(self) -> None:
        self._handle.set_value(self._initial_value)


class SetParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, value: any) -> None:
        super(SetParam, self).__init__(parameter)
        self._value = value

    def _update(self, adj_progress: float, duration: float) -> None:
        self._handle.set_value(self._value)


class InterpParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, from_val: any = None, to_val: any = None):
        super(InterpParam, self).__init__(parameter)
        self._from_val = from_val
        self._to_val = to_val

    def _interp(self, p: float) -> float:
        if self._from_val is None or self._to_val is None:
            return self._handle.get_value()

        return self._from_val + (self._to_val - self._from_val) * p

    def _update(self, adj_progress: float, duration: float) -> None:
        self._handle.set_value(self._interp(adj_progress))
