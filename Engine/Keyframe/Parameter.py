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
        self._pre_value = parameter.get_value()

    def reset(self) -> None:
        self._handle.set_value(self._pre_value)


class SetParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, value: any) -> None:
        super(SetParam, self).__init__(parameter)
        self._f_value = value

    def _update(self, adj_progress: float, duration: float) -> None:
        self._handle.set_value(self._f_value)


class InterpParam(ParameterKeyframeObject):
    def __init__(self, parameter: Parameter, i_val: any = None, f_val: any = None):
        super(InterpParam, self).__init__(parameter)
        self._i_value = i_val
        self._f_value = f_val

    def _update(self, adj_progress: float, duration: float) -> None:
        self._handle.set_value(self._interp(adj_progress))
