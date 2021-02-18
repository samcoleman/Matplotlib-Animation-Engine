from Engine.MathsHelpers import Vec2D, Vec3D
from Engine.Keyframe.Keyframe import KeyFrameObject
from typing import Union

from Engine.Elements.BasicElements import TextElement
from Engine.Elements.AxesElement import AxesElement


class Transform(KeyFrameObject):
    def __init__(self, end: Union[float, Vec2D, Vec3D], absolute: bool = True):
        super(Transform, self).__init__()
        self._start = None
        self._end = end
        self._abs = absolute
        self._rel_end = None

    def _interp(self, p):
        return self._start + (self._end - self._start) * p

    def _post_start(self):
        if self._end is None or self._start is None:
            return

        if self._abs is False and self._rel_end is None:
            self._rel_end = self._end
            self._end = self._start + self._rel_end


class TranslateX(Transform):
    def __init__(self, end: float, absolute: bool = True):
        super(TranslateX, self).__init__(end, absolute)

    def _set_start(self):
        if isinstance(self._handle, TextElement):
            start_pos = self._handle.get_text().get_position()
            self._start = start_pos[0]
        elif isinstance(self._handle, AxesElement):
            self._start = self._handle.get_axes().get_position().x0

    def _update(self, adj_progress: float):
        if isinstance(self._handle, TextElement):
            new_pos_x = self._interp(adj_progress)
            current_pos = self._handle.get_text().get_position()
            self._handle.get_text().set_position((new_pos_x, current_pos[1]))
        elif isinstance(self._handle, AxesElement):
            new_pos_x = self._interp(adj_progress)
            # Returns Bbox [[x0, y0], [x1, y1]]
            current_state = self._handle.get_axes().get_position()
            width = current_state.x1 - current_state.x0
            current_state.x0 = new_pos_x
            current_state.x1 = new_pos_x + width
            self._handle.get_axes().set_position(current_state)


class TranslateY(Transform):
    def __init__(self, end: float, absolute: bool = True):
        super(TranslateY, self).__init__(end, absolute)

    def _set_start(self):
        if isinstance(self._handle, TextElement):
            start_pos = self._handle.get_text().get_position()
            self._start = start_pos[1]
        elif isinstance(self._handle, AxesElement):
            self._start = self._handle.get_axes().get_position().y0

    def _update(self, adj_progress: float):
        if isinstance(self._handle, TextElement):
            new_pos_y = self._interp(adj_progress)
            current_pos = self._handle.get_text().get_position()
            self._handle.get_text().set_position((current_pos[0], new_pos_y))
        elif isinstance(self._handle, AxesElement):
            new_pos_y = self._interp(adj_progress)
            # Returns Bbox [[x0, y0], [x1, y1]]
            current_state = self._handle.get_axes().get_position()
            height = current_state.y1 - current_state.y0
            current_state.y0 = new_pos_y
            current_state.y1 = new_pos_y + height
            self._handle.get_axes().set_position(current_state)


class Translate2D(Transform):
    def __init__(self, end: Vec2D, absolute: bool = True):
        super(Translate2D, self).__init__(end, absolute)

    def _set_start(self):
        if isinstance(self._handle, TextElement):
            self._start = Vec2D(self._handle.get_text().get_position())
        elif isinstance(self._handle, AxesElement):
            self._start = Vec2D(self._handle.get_axes().get_position().x0, self._handle.get_axes().get_position().y0)

    def _update(self, adj_progress: float):
        if isinstance(self._handle, TextElement):
            new_pos = self._interp(adj_progress)
            self._handle.get_text().set_position(new_pos)
        elif isinstance(self._handle, AxesElement):
            new_pos = self._interp(adj_progress)
            # Returns Bbox [[x0, y0], [x1, y1]]
            current_state = self._handle.get_axes().get_position()
            width = current_state.x1 - current_state.x0
            height = current_state.y1 - current_state.y0
            self._handle.get_axes().set_position((new_pos.x, new_pos.y, width, height))


class Rotate(Transform):
    def __init__(self, end: float, origin: Vec2D = Vec2D(0, 0), absolute: bool = True):
        # Minus is to make positive rotations clockwise
        super(Rotate, self).__init__(-end, absolute)
        self._origin = origin

    def _set_start(self):
        if isinstance(self._handle, TextElement):
            self._start = self._handle.get_text().get_rotation()
        elif isinstance(self._handle, AxesElement):
            # Not worked this out yet
            return

    def _update(self, adj_progress: float):
        if isinstance(self._handle, TextElement):
            new_rot = self._interp(adj_progress)
            self._handle.get_text().set_rotation(new_rot)
        elif isinstance(self._handle, AxesElement):
            # Not worked this out yet
            return


class Scale(Transform):
    def __init__(self, end: float, origin: Vec2D = Vec2D(0, 0), absolute: bool = False):
        super(Scale, self).__init__(end, absolute)
        self._origin = origin

    def _post_start(self):
        if self._end is None or self._start is None:
            return

        if self._abs is False and self._rel_end is None:
            self._rel_end = self._end
            self._end = self._start * self._rel_end

    def _set_start(self):
        if isinstance(self._handle, TextElement):
            self._start = self._handle.get_text().get_fontsize()
        elif isinstance(self._handle, AxesElement):
            current_state = self._handle.get_axes().get_position()
            width = current_state.x1 - current_state.x0
            height = current_state.y1 - current_state.y0
            self._start = Vec2D(width, height)

    def _update(self, adj_progress: float):
        if isinstance(self._handle, TextElement):
            new_size = self._interp(adj_progress)
            self._handle.get_text().set_fontsize(new_size)
        elif isinstance(self._handle, AxesElement):
            new_size = self._interp(adj_progress)
            current_state = self._handle.get_axes().get_position()
            current_state.x1 = current_state.x0 + new_size.x
            current_state.y1 = current_state.y0 + new_size.y
            self._handle.get_axes().set_position(current_state)


class Scale2D(Transform):
    def __init__(self, end: Vec2D, origin: Vec2D = Vec2D(0, 0), absolute: bool = False):
        super(Scale2D, self).__init__(end, absolute)
        self._origin = origin

    def _post_start(self):
        if self._end is None or self._start is None:
            return

        if self._abs is False and self._rel_end is None:
            self._rel_end = self._end
            # Equivalent to dot product, not sure why can't just multiply?
            self._end.x = self._start.x * self._rel_end.x
            self._end.y = self._start.y * self._rel_end.y

    def _set_start(self):
        if isinstance(self._handle, TextElement):
            # N/A?
            return
        elif isinstance(self._handle, AxesElement):
            current_state = self._handle.get_axes().get_position()
            width = current_state.x1 - current_state.x0
            height = current_state.y1 - current_state.y0
            self._start = Vec2D(width, height)

    def _update(self, adj_progress: float):
        if isinstance(self._handle, TextElement):
            # N/A?
            return
        elif isinstance(self._handle, AxesElement):
            new_size = self._interp(adj_progress)
            current_state = self._handle.get_axes().get_position()
            current_state.x1 = current_state.x0 + new_size.x
            current_state.y1 = current_state.y0 + new_size.y
            self._handle.get_axes().set_position(current_state)
