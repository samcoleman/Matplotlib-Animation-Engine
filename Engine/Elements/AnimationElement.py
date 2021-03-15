from Engine.MathsHelpers import Vec2D
from Engine.Keyframe.Keyframe import KeyFrameManager

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.text import Text

from Engine.Keyframe.Keyframe import KeyFrame
from Engine.Keyframe.Parameter import GlobalParameterManager, Parameter


from typing import Union, Dict, List


# Animation Element, start time and end time
class AnimationElement:
    def __init__(self, position: Vec2D) -> None:
        self._instantiated = False
        self._start, self._end = 0, 0

        self._main_fig: Union[None, Figure] = None
        self._main_axes: Union[None, Axes] = None

        self._instance_id: Union[None, str] = None
        self._global_parameter_manager: Union[None, GlobalParameterManager] = None

        self._position = position

        self._keyframeMng = KeyFrameManager()
        self._parameters: Dict[str, Parameter] = dict()

    # Removed this functionality, my be reused if keyframes and parameters unified
    # def attach_sequence(self, sequence: List[KeyFrame], handle: any = None) -> None:
    def attach_sequence(self, sequence: List[KeyFrame]) -> None:
        # if handle is None:
        self._keyframeMng.attach_sequence(sequence)
        # else:
        #     self._keyframeMng.attach_sequence(sequence, handle)

    def attach_timings(self, start: float, end: float) -> None:
        self._start = start
        self._end = end

    def attach_parameter_manager(self, instance_id: str, param_manager: GlobalParameterManager) -> None:
        self._instance_id = instance_id

        self._global_parameter_manager = param_manager
        self._global_parameter_manager.attach_local_parameters(self._instance_id, self._parameters)

    def _create_parameter(self, local_key: str, param: Parameter) -> Parameter:
        self._parameters[local_key] = param
        return param

    def _get_parameter(self, local_key: str) -> Parameter:
        return self._parameters[local_key]

    # Saves having to write .get_value()
    def _get_parameter_value(self, local_key: str) -> any:
        return self._parameters[local_key].get_value()

    def get_parameters(self) -> Dict[str, Parameter]:
        return self._parameters

    def get_timings(self) -> (float, float):
        return self._start, self._end

    def attach_main_scene(self, main_fig: Figure, main_axes: Axes) -> None:
        self._main_fig = main_fig
        self._main_axes = main_axes

    # Return types so far
    # Might regret this?
    def _get_handle(self) -> Union[None, Axes, Text]:
        return

    # These are separated for ease of use later so super() call is not needed
    # Used to draw element onto the main_fig/main_axes
    def _inset(self) -> None:
        return

    def instantiate(self) -> None:
        self._instantiate()
        self._keyframeMng.attach_handle(self._get_handle())

    # Used to initialise the element
    def _instantiate(self) -> None:
        return

    def update(self, progress: float, duration: float) -> None:
        if self._instantiated is False:
            self._instantiated = True
            self._inset()
            self.instantiate()

        self._keyframeMng.update(progress, duration)
        self._update(progress, duration)

    # Used to update element
    def _update(self, progress: float, duration: float) -> None:
        return

    def cleanup(self) -> None:
        if self._instantiated is True:
            self._instantiated = False
            self._cleanup()

    # Cleanup element
    def _cleanup(self) -> None:
        return
