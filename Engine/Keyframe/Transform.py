from Engine.MathsHelpers import Vec2D, Vec3D
from Engine.Keyframe.Keyframe import KeyframeObject
from typing import Union

from matplotlib.axes import Axes
from matplotlib.text import Text


class Transform(KeyframeObject):
    def __init__(self, f_value: Union[float, Vec2D, Vec3D], absolute: bool = False):
        super(Transform, self).__init__()
        self._i_value: Union[None, type(f_value)] = None
        self._f_value = f_value
        self._abs = absolute
        self._rel_f_value = None

    def _post_start(self):
        if self._f_value is None or self._i_value is None:
            return

        if self._abs is False and self._rel_f_value is None:
            self._rel_f_value = self._f_value
            self._f_value = self._i_value + self._rel_f_value


class TranslateX(Transform):
    def __init__(self, end: float, absolute: bool = False):
        super(TranslateX, self).__init__(end, absolute)

    def _set_start(self):
        if isinstance(self._handle, Text):
            start_pos = self._handle.get_position()
            self._i_value = start_pos[0]
        elif isinstance(self._handle, Axes):
            self._i_value = self._handle.get_position().x0

    def _update(self, adj_progress: float, duration: float):
        if isinstance(self._handle, Text):
            new_pos_x = self._interp(adj_progress)
            current_pos = self._handle.get_position()
            self._handle.set_position((new_pos_x, current_pos[1]))
        elif isinstance(self._handle, Axes):
            new_pos_x = self._interp(adj_progress)
            # Returns Bbox [[x0, y0], [x1, y1]]
            current_state = self._handle.get_position()
            width = current_state.x1 - current_state.x0
            current_state.x0 = new_pos_x
            current_state.x1 = new_pos_x + width
            self._handle.set_position(current_state)


class TranslateY(Transform):
    def __init__(self, end: float, absolute: bool = False):
        super(TranslateY, self).__init__(end, absolute)

    def _set_start(self):
        if isinstance(self._handle, Text):
            start_pos = self._handle.get_position()
            self._i_value = start_pos[1]
        elif isinstance(self._handle, Axes):
            self._i_value = self._handle.get_position().y0

    def _update(self, adj_progress: float, duration: float):
        if isinstance(self._handle, Text):
            new_pos_y = self._interp(adj_progress)
            current_pos = self._handle.get_position()
            self._handle.set_position((current_pos[0], new_pos_y))
        elif isinstance(self._handle, Axes):
            new_pos_y = self._interp(adj_progress)
            # Returns Bbox [[x0, y0], [x1, y1]]
            current_state = self._handle.get_position()
            height = current_state.y1 - current_state.y0
            current_state.y0 = new_pos_y
            current_state.y1 = new_pos_y + height
            self._handle.set_position(current_state)


class Translate2D(Transform):
    def __init__(self, end: Vec2D, absolute: bool = False):
        super(Translate2D, self).__init__(end, absolute)

    def _set_start(self):
        if isinstance(self._handle, Text):
            self._i_value = Vec2D(self._handle.get_position())
        elif isinstance(self._handle, Axes):
            self._i_value = Vec2D(self._handle.get_position().x0, self._handle.get_position().y0)

    def _update(self, adj_progress: float, duration: float):
        if isinstance(self._handle, Text):
            new_pos = self._interp(adj_progress)
            self._handle.set_position(new_pos)
        elif isinstance(self._handle, Axes):
            new_pos = self._interp(adj_progress)
            # Returns Bbox [[x0, y0], [x1, y1]]
            current_state = self._handle.get_position()
            width = current_state.x1 - current_state.x0
            height = current_state.y1 - current_state.y0
            self._handle.set_position((new_pos.x, new_pos.y, width, height))


class Rotate(Transform):
    def __init__(self, end: float, origin: Vec2D = Vec2D(0, 0), absolute: bool = False):
        # Minus is to make positive rotations clockwise
        super(Rotate, self).__init__(-end, absolute)
        self._origin = origin

    def _set_start(self):
        if isinstance(self._handle, Text):
            self._i_value = self._handle.get_rotation()
        elif isinstance(self._handle, Axes):
            # Not worked this out yet
            return

    def _update(self, adj_progress: float, duration: float):
        if isinstance(self._handle, Text):
            new_rot = self._interp(adj_progress)
            self._handle.set_rotation(new_rot)
        elif isinstance(self._handle, Axes):
            # Not worked this out yet
            return


class Scale(Transform):
    def __init__(self, end: float, origin: Vec2D = Vec2D(0, 0), absolute: bool = False):
        super(Scale, self).__init__(end, absolute)
        self._origin = origin

    def _post_start(self):
        if self._f_value is None or self._i_value is None:
            return

        if self._abs is False and self._rel_f_value is None:
            self._rel_f_value = self._f_value
            self._f_value = self._i_value * self._rel_f_value

    def _set_start(self):
        if isinstance(self._handle, Text):
            self._i_value = self._handle.get_fontsize()
        elif isinstance(self._handle, Axes):
            current_state = self._handle.get_position()
            width = current_state.x1 - current_state.x0
            height = current_state.y1 - current_state.y0
            self._i_value = Vec2D(width, height)

    def _update(self, adj_progress: float, duration: float):
        if isinstance(self._handle, Text):
            new_size = self._interp(adj_progress)
            self._handle.set_fontsize(new_size)
        elif isinstance(self._handle, Axes):
            new_size = self._interp(adj_progress)
            current_state = self._handle.get_position()
            current_state.x1 = current_state.x0 + new_size.x
            current_state.y1 = current_state.y0 + new_size.y
            self._handle.set_position(current_state)


class Scale2D(Transform):
    def __init__(self, end: Vec2D, origin: Vec2D = Vec2D(0, 0), absolute: bool = False):
        super(Scale2D, self).__init__(end, absolute)
        self._origin = origin

    def _post_start(self):
        if self._f_value is None or self._i_value is None:
            return

        if self._abs is False and self._rel_f_value is None:
            self._rel_f_value = self._f_value
            # Equivalent to dot product, not sure why can't just multiply?
            self._f_value.x = self._i_value.x * self._rel_f_value.x
            self._f_value.y = self._i_value.y * self._rel_f_value.y

    def _set_start(self):
        if isinstance(self._handle, Text):
            # N/A?
            return
        elif isinstance(self._handle, Axes):
            current_state = self._handle.get_position()
            width = current_state.x1 - current_state.x0
            height = current_state.y1 - current_state.y0
            self._i_value = Vec2D(width, height)

    def _update(self, adj_progress: float, duration: float):
        if isinstance(self._handle, Text):
            # N/A?
            return
        elif isinstance(self._handle, Axes):
            new_size = self._interp(adj_progress)
            current_state = self._handle.get_position()
            current_state.x1 = current_state.x0 + new_size.x
            current_state.y1 = current_state.y0 + new_size.y
            self._handle.set_position(current_state)
