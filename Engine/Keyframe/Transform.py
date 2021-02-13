from Engine.MathsHelpers import Vec2D, Vec3D
from Engine.Keyframe.Keyframe import KeyFrameObject
from typing import Union


class Transform(KeyFrameObject):
    def __init__(self, end: Union[float, Vec2D, Vec3D], absolute: bool = True):
        super(Transform, self).__init__()
        self._end = end
        self._abs = absolute
        self._rel_end = None

    def post_start(self):
        if self._abs is False and self._rel_end is None:
            self._rel_end = self._end
            self._end = self._start + self._rel_end


class TranslateX(Transform):
    def __init__(self, end: float, absolute: bool = True):
        super(TranslateX, self).__init__(end, absolute)

    def set_start_text(self):
        start_pos = self._handle.get_position()
        self._start = start_pos[0]

    def set_start_axes(self):
        self._start = self._handle.get_position().x0

    def update_text(self, adj_progress: float):
        new_pos_x = self.interp(adj_progress)
        current_pos = self._handle.get_position()
        self._handle.set_position((new_pos_x, current_pos[1]))

    def update_axes(self, adj_progress: float):
        new_pos_x = self.interp(adj_progress)
        # Returns Bbox [[x0, y0], [x1, y1]]
        current_state = self._handle.get_position()
        width = current_state.x1 - current_state.x0
        current_state.x0 = new_pos_x
        current_state.x1 = new_pos_x + width
        self._handle.set_position(current_state)


class TranslateY(Transform):
    def __init__(self, end: float, absolute: bool = True):
        super(TranslateY, self).__init__(end, absolute)

    def set_start_text(self):
        start_pos = self._handle.get_position()
        self._start = start_pos[1]

    def set_start_axes(self):
        self._start = self._handle.get_position().y0

    def update_text(self, adj_progress: float):
        new_pos_y = self.interp(adj_progress)
        current_pos = self._handle.get_position()
        self._handle.set_position((current_pos[0], new_pos_y))

    def update_axes(self, adj_progress: float):
        new_pos_y = self.interp(adj_progress)
        # Returns Bbox [[x0, y0], [x1, y1]]
        current_state = self._handle.get_position()
        height = current_state.y1 - current_state.y0
        current_state.y0 = new_pos_y
        current_state.y1 = new_pos_y + height
        self._handle.set_position(current_state)


class Translate2D(Transform):
    def __init__(self, end: Vec2D, absolute: bool = True):
        super(Translate2D, self).__init__(end, absolute)

    def set_start_text(self):
        self._start = Vec2D(self._handle.get_position())

    def set_start_axes(self):
        self._start = Vec2D(self._handle.get_position().x0, self._handle.get_position().y0)

    def update_text(self, adj_progress: float):
        new_pos = self.interp(adj_progress)
        self._handle.set_position(new_pos)

    def update_axes(self, adj_progress: float):
        new_pos = self.interp(adj_progress)
        # Returns Bbox [[x0, y0], [x1, y1]]
        current_state = self._handle.get_position()
        width = current_state.x1 - current_state.x0
        height = current_state.y1 - current_state.y0
        self._handle.set_position((new_pos.x, new_pos.y, width, height))


class Rotate(Transform):
    def __init__(self, end: float, origin: Vec2D = Vec2D(0, 0), absolute: bool = True):
        # Minus is to make positive rotations clockwise
        super(Rotate, self).__init__(-end, absolute)
        self._origin = origin

    def set_start_text(self):
        self._start = self._handle.get_rotation()

    def update_text(self, adj_progress: float):
        new_rot = self.interp(adj_progress)
        self._handle.set_rotation(new_rot)


class Scale(Transform):
    def __init__(self, end: float, origin: Vec2D = Vec2D(0, 0), absolute: bool = False):
        super(Scale, self).__init__(end, absolute)
        self._origin = origin

    def post_start(self):
        if self._abs is False and self._rel_end is None:
            self._rel_end = self._end
            self._end = self._start * self._rel_end

    def set_start_text(self):
        self._start = self._handle.get_fontsize()

    def set_start_axes(self):
        current_state = self._handle.get_position()
        width = current_state.x1 - current_state.x0
        height = current_state.y1 - current_state.y0
        self._start = Vec2D(width, height)

    def update_text(self, adj_progress: float):
        new_size = self.interp(adj_progress)
        self._handle.set_fontsize(new_size)

    def update_axes(self, adj_progress: float):
        new_size = self.interp(adj_progress)
        current_state = self._handle.get_position()
        current_state.x1 = current_state.x0 + new_size.x
        current_state.y1 = current_state.y0 + new_size.y
        self._handle.set_position(current_state)


class Scale2D(Transform):
    def __init__(self, end: Vec2D, origin: Vec2D = Vec2D(0, 0), absolute: bool = False):
        super(Scale2D, self).__init__(end, absolute)
        self._origin = origin

    def post_start(self):
        if self._abs is False and self._rel_end is None:
            self._rel_end = self._end
            # Equivalent to dot production, not sure why can't just multiply?
            self._end.x = self._start.x * self._rel_end.x
            self._end.y = self._start.y * self._rel_end.y

    def set_start_axes(self):
        current_state = self._handle.get_position()
        width = current_state.x1 - current_state.x0
        height = current_state.y1 - current_state.y0
        self._start = Vec2D(width, height)

    def update_axes(self, adj_progress: float):
        new_size = self.interp(adj_progress)
        current_state = self._handle.get_position()
        current_state.x1 = current_state.x0 + new_size.x
        current_state.y1 = current_state.y0 + new_size.y
        self._handle.set_position(current_state)

"""
class Transform(Interpolate):
    def __init__(self, end: Union[float, Vec2D, Vec3D], absolute=True, fn=lambda y: y):
        super(Transform, self).__init__(end, fn)
        self._abs = absolute
        self._rel_end = end

    def set_start(self, start: Union[float, Vec2D, Vec3D]):
        if self._start is not start:
            self._start = start

        if not self._abs:
            self._end = self._start + self._rel_end



Transform_Keyframe = Tuple[Union[List[Transform], Transform], float]
Transform_Sequence = Union[List[Transform_Keyframe], None]


class Translate2D(Transform):
    def __init__(self, end: Vec2D, absolute=True, fn=lambda y: y):
        super(Translate2D, self).__init__(end, absolute, fn)


class Rotate(Transform):
    def __init__(self, end: float, absolute=True, fn=lambda y: y):
        super(Rotate, self).__init__(end, absolute, fn)


class Scale(Transform):
    def __init__(self, end: float, absolute=True, fn=lambda y: y):
        super(Scale, self).__init__(end, absolute, fn)

    def set_start(self, start: float):
        if self._start is not start:
            self._start = start

        if not self._abs:
            self._end = self._start * self._rel_end


class Scale2D(Transform):
    def __init__(self, end: Vec2D, absolute=True, fn=lambda y: y):
        super(Scale2D, self).__init__(end, absolute, fn)
        print("init")
        self._rel_end = end

    def set_start(self, start: Vec2D):
        if self._start is not start:
            self._start = start

        # somethings is setting rel_end fuck knows what
        if not self._abs:
            self._end.x = self._start.x * float(self._rel_end.x)

        print(self._start)
        print(self._end)
        print(self._rel_end)


class TextTransform:
    def __init__(self, s: Transform_Sequence, text, start_pos: Vec2D, start_rot: float, start_size: float):
        self._s = s
        self._text = text
        self._s_pos = start_pos
        self._s_rot = start_rot
        self._s_size = start_size

    def update(self, p):
        if self._s is None:
            return self._s_pos, self._s_rot, self._s_size

        last_key_time = 0

        last_key_pos = self._s_pos
        last_key_rot = self._s_rot
        last_key_size = self._s_size

        def progress_interp(last_key, current_key, progress):
            return (progress - last_key)/(current_key-last_key)

        def trn(t, l_k, l_k_t, pro, k_t):
            t.set_start(l_k)
            return t.interp(progress_interp(l_k_t, k_t, pro))

        for keyframe in self._s:
            # Very ugly stops for loop tripping up when transform is not a list
            k = keyframe[0]
            if issubclass(type(keyframe[0]), Interpolate):
                k = [keyframe[0]]

            for transform in k:
                if type(transform) is Translate2D:
                    last_key_pos = trn(transform, last_key_pos, last_key_time, p, keyframe[1])
                    self._text.set_position((last_key_pos.x, last_key_pos.y))
                if type(transform) is Rotate:
                    last_key_rot = trn(transform, last_key_rot, last_key_time, p, keyframe[1])
                    self._text.set_rotation(-last_key_rot)
                if type(transform) is Scale:
                    last_key_size = trn(transform, last_key_size, last_key_time, p, keyframe[1])
                    self._text.set_size(last_key_size)
            last_key_time = keyframe[1]

        # Return new state
        return last_key_pos, last_key_rot, last_key_size


class AxesTransform:
    def __init__(self, s: Transform_Sequence, axes, start_pos: Vec2D, start_rot: float, start_size: Vec2D):
        self._s = s
        self._axes = axes
        self._s_pos = start_pos
        self._s_rot = start_rot
        self._s_size = start_size

    def update(self, p):

        if self._s is None:
            return self._s_pos, self._s_rot, self._s_size

        last_key_time = 0

        last_key_pos = self._s_pos
        last_key_rot = self._s_rot
        last_key_size = self._s_size

        def progress_interp(last_key, current_key, progress):
            return (progress - last_key)/(current_key-last_key)

        def trn(t, l_k, l_k_t, pro, k_t):
            t.set_start(l_k)
            return t.interp(progress_interp(l_k_t, k_t, pro))

        for keyframe in self._s:
            # Very ugly stops for loop tripping up when transform is not a list
            k = keyframe[0]
            if issubclass(type(keyframe[0]), Interpolate):
                k = [keyframe[0]]

            for transform in k:
                if type(transform) is Translate2D:
                    last_key_pos = trn(transform, last_key_pos, last_key_time, p, keyframe[1])
                    self._axes.set_position((last_key_pos.x, last_key_pos.y, last_key_size.x, last_key_size.y))
                # Add rotation feature?

                # if type(transform) is Rotate:
                    # last_key_rot = trn(transform, last_key_rot, last_key_time, p, keyframe[1])
                    # self._text.set_rotation(last_key_rot)

                #Add 1D scaling? aspect ratio issues

                #if type(transform) is Scale:
                #    last_key_size.y = trn(transform, last_key_size.y, last_key_time, p, keyframe[1])
                #    last_key_size.y = last_key_size.y
                #    self._axes.set_position((last_key_pos.x, last_key_pos.y, last_key_size.x, last_key_size.y))
                if type(transform) is Scale2D:
                    last_key_size = trn(transform, last_key_size, last_key_time, p, keyframe[1])
                    self._axes.set_position((last_key_pos.x, last_key_pos.y, last_key_size.x, last_key_size.y))
            last_key_time = keyframe[1]

        # Return new state
        return last_key_pos, last_key_rot, last_key_size

"""


