
from myMaths import Vec2D, Vec3D
from typing import List, Tuple, Union


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class T:
    def __init__(self, end: Union[float, Vec2D, Vec3D], fn=lambda y: y):
        self._start = 1
        self._end = end
        self._fn = fn

    def set_start(self, start: Union[float, Vec2D, Vec3D]):
        self._start = start

    def interp(self, p):
        print(self._start)
        print(self._end)
        return self._start + (self._end - self._start) * clamp(self._fn(p), 0, 1)


Keyframe = Tuple[Union[List[T], T], float]
Sequence = Union[List[Keyframe], None]


class Translate2D(T):
    def __init__(self, end: Vec2D, fn=lambda y: y):
        super(Translate2D, self).__init__(end, fn)


class Rotate(T):
    def __init__(self, end: float, fn=lambda y: y):
        super(Rotate, self).__init__(end, fn)


class Scale(T):
    def __init__(self, end: float, fn=lambda y: y):
        super(Scale, self).__init__(end, fn)


class Scale2D(T):
    def __init__(self, end: Vec2D, fn=lambda y: y):
        super(Scale2D, self).__init__(end, fn)


class TextTransform:
    def __init__(self, s: Sequence, text, start_pos: Vec2D, start_rot: float, start_size: float):
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
            if issubclass(type(keyframe[0]), T):
                k = [keyframe[0]]

            for transform in k:
                if type(transform) is Translate2D:
                    last_key_pos = trn(transform, last_key_pos, last_key_time, p, keyframe[1])
                    self._text.set_position((last_key_pos.x, last_key_pos.y))
                if type(transform) is Rotate:
                    last_key_rot = trn(transform, last_key_rot, last_key_time, p, keyframe[1])
                    self._text.set_rotation(last_key_rot)
                if type(transform) is Scale:
                    last_key_size = trn(transform, last_key_size, last_key_time, p, keyframe[1])
                    self._text.set_size(last_key_size)
            last_key_time = keyframe[1]

        # Return new state
        return last_key_pos, last_key_rot, last_key_size


class AxesTransform:
    def __init__(self, s: Sequence, axes, start_pos: Vec2D, start_rot: float, start_size: Vec2D):
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
            if issubclass(type(keyframe[0]), T):
                k = [keyframe[0]]

            for transform in k:
                if type(transform) is Translate2D:
                    last_key_pos = trn(transform, last_key_pos, last_key_time, p, keyframe[1])
                    self._axes.set_position((last_key_pos.x, last_key_pos.y, last_key_size.x, last_key_size.y))
                # if type(transform) is Rotate:
                    # last_key_rot = trn(transform, last_key_rot, last_key_time, p, keyframe[1])
                    # self._text.set_rotation(last_key_rot)
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




