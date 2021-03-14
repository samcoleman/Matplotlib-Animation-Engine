from Engine.MathsHelpers import Vec2D
from Engine.Keyframe.Keyframe import KeyFrameManager

from matplotlib.figure import Figure
from matplotlib.axes import Axes

from Engine.Keyframe.Parameter import GlobalParameterManager, Parameter

from typing import Dict


# Animation Element, start time and end time
class AnimationElement:
    def __init__(self, position: Vec2D):
        self._instantiated = False
        self._start, self._end = 0, 0
        self._main_fig, self._main_axes = None, None

        # Double underscore as _attach_parameter & _get_parameter should only be used
        self._instance_id, self.__global_parameter_manager = None, None

        self._position = position

        self._keyframeMng = KeyFrameManager()

        self._parameters: Dict[str, Parameter] = dict()
        #self._parameters: List[Parameter] = []

    def attach_keyframes(self, k, handle=None):
        if handle is None:
            self._keyframeMng.attach_keyframes(k, self)
        else:
            self._keyframeMng.attach_keyframes(k, handle)

    def attach_timings(self, start: float, end: float):
        self._start = start
        self._end = end

    def attach_parameter_manager(self, instance_id: str, param_manager: GlobalParameterManager):
        self._instance_id = instance_id
        self.__global_parameter_manager = param_manager

        # Attach the local parameters globally / for browse editing of parameters omitted until implemented
        #for local_key in self._parameters:
        #    self.__global_parameter_manager.attach_parameter(self._instance_id + local_key, self._parameters[local_key])

    def _create_parameter(self, local_key: str, param: Parameter):
        self._parameters[local_key] = param
        return param

    def _get_parameter(self, local_key: str):
        return self._parameters[local_key]

        # Merger of local parameters doesnt update the global manager
        #return self.__global_parameter_manager.get_parameter(self._instance_id+local_key)

    # Saves havign to write .get_value()
    def _get_parameter_value(self, local_key: str):
        return self._parameters[local_key].get_value()

    def get_parameters(self):
        return self._parameters

    def get_timings(self):
        return self._start, self._end

    def attach_main_scene(self, main_fig: Figure, main_axes: Axes):
        self._main_fig = main_fig
        self._main_axes = main_axes

    # These are separated for ease of use later so super() call is not needed
    # Used to draw element onto the main_fig/main_axes
    def _inset(self):
        return

    # Used to initialise the element
    def _instantiate(self):
        return

    def update(self, progress: float, duration: float):
        if self._instantiated is False:
            self._instantiated = True
            self._inset()
            self._instantiate()

        self._keyframeMng.update(progress, duration)
        self._update(progress, duration)

    # Used to update element
    def _update(self, progress: float, duration: float):
        return

    def cleanup(self):
        if self._instantiated is True:
            self._instantiated = False
            self._cleanup()

    # Cleanup element
    def _cleanup(self):
        return
