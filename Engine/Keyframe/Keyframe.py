from typing import List, Union

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class KeyFrameObject:
    def __init__(self):
        self._handle = None

    def attach_handle(self, h):
        # Only attach handle if there is not one already
        if self._handle is None:
            self._handle = h

    # Call relevant start function function depending on handle type
    def set_start(self):
        self._set_start()
        self._post_start()

    def _set_start(self):
        return 0

    # This function is called after start handle is called
    def _post_start(self):
        return 0

    # Call relevant update function function depending on handle type
    def update(self, adj_progress: float):
        self._update(adj_progress)
        self._post_update(adj_progress)

    def _update(self, adj_progress: float):
        return 0

    # This function is called after update handle is called
    def _post_update(self, adj_progress: float):
        return 0


class KeyFrame:
    def __init__(self, keyobjs: List[KeyFrameObject], end_t: float, start_t: Union[float, None] = None, fn=lambda y: y):
        self._key_objs = keyobjs
        self._start_t = start_t
        self._end_t = end_t
        self._fn = fn

    def set_start(self, start: float):
        self._start_t = start

    def get_start(self):
        return self._start_t

    def get_end(self):
        return self._end_t

    def attach_handle(self, h):
        for keyobj in self._key_objs:
            keyobj.attach_handle(h)

    def update(self, progress: float):
        # Potench just needs a 0 clamp as should never be above 1?
        adjusted_progress = clamp((progress - self._start_t)/(self._end_t-self._start_t), 0, 1)
        for key in self._key_objs:
            if adjusted_progress == 0:
                key.set_start()

            key.update(self._fn(adjusted_progress))


class KeyFrameManager:
    def __init__(self):
        self._keyframes = None

    def attach_keyframes(self, keyframes: List[KeyFrame], handle):
        self._keyframes = keyframes

        # Setup the start time for each keyframe
        for i in range(len(self._keyframes)):
            if self._keyframes[i].get_start() is None:
                if i == 0:
                    # Set start time to 0 if the first item
                    self._keyframes[i].set_start(0)
                else:
                    # Otherwise set to the end-time of previous keyframe
                    self._keyframes[i].set_start(self._keyframes[i-1].get_end())

            self._keyframes[i].attach_handle(handle)

    def attach_handle(self, h):
        if self._keyframes is None:
            # Cannot attach handles if keyframes don't exist
            return

        for key in self._keyframes:
            key.attach_handle(h)

    def update(self, progress: float):
        if self._keyframes is None:
            # Exit if keyframes have not been attached
            return

        for key in self._keyframes:
            if progress < key.get_end():
                key.update(progress)


