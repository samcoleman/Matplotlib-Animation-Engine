from typing import List, Union
import operator


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class KeyframeObject:
    def __init__(self):
        self._handle = None
        self._set_s = False

    def attach_handle(self, h):
        # Only attach handle if there is not one already
        if self._handle is None:
            self._handle = h

    def set_start(self):
        self._set_start()
        self._post_start()

    def _set_start(self):
        return 0

    def _post_start(self):
        return 0

    def update(self, adj_progress: float, duration: float):
        self._update(adj_progress, duration)
        self._post_update(adj_progress, duration)

    def _update(self, adj_progress: float, duration: float):
        return 0

    # This function is called after update handle is called
    def _post_update(self, adj_progress: float, duration: float):
        return 0


class KeyFrame:
    def __init__(self, keyobjs: List[KeyframeObject], end_t: float, start_t: Union[float, None] = None, fn=lambda y: y):
        self._update_start_called = False
        self._key_objs = keyobjs
        self._start_t = start_t
        self._end_t = end_t
        self._fn = fn

    def set_start_time(self, start: float):
        self._start_t = start

    def get_start_time(self):
        return self._start_t

    def get_end_time(self):
        return self._end_t

    def attach_handle(self, h):
        for key in self._key_objs:
            key.attach_handle(h)

    def update_start(self):
        if self._update_start_called is False:
            for key in self._key_objs:
                key.set_start()
        else:
            print("repeat start call")

            self._update_start_called = True

    def update(self, progress: float, duration: float):
        adjusted_progress = clamp((progress - self._start_t)/(self._end_t-self._start_t), 0, 1)

        for key in self._key_objs:
            # Hmm might cause problems for duration? Not that im using for alt yet
            key.update(self._fn(adjusted_progress), duration)


class KeyFrameManager:
    def __init__(self):
        self._keyframes = None
        self._last_progress, self._max_progress = 0, 0
        self._start_baked = False

    def attach_keyframes(self, keyframes: List[KeyFrame], handle):
        self._keyframes = keyframes

        # Setup the start time for each keyframe if not already set, allows for quick keyframing
        for i in range(len(self._keyframes)):
            if self._keyframes[i].get_start_time() is None:
                if i == 0:
                    # Set start time to 0 if the first item
                    self._keyframes[i].set_start_time(0)
                else:
                    # Otherwise set to the end-time of previous keyframe
                    self._keyframes[i].set_start_time(self._keyframes[i-1].get_end_time())

            self._keyframes[i].attach_handle(handle)

        # Sort keyframe so they appear in ascending order by _start_t
        # Should help resolve user input errors and be more consistent
        self._keyframes = sorted(self._keyframes, key=operator.attrgetter('_start_t'))
        # Inplace sort, use if memory is a problem but really doubt it
        #x.sort(key=operator.attrgetter('score'))

    def attach_handle(self, h):
        if self._keyframes is None:
            # Cannot attach handles if keyframes don't exist
            return

        for key in self._keyframes:
            key.attach_handle(h)

    # The whole sequence is run through in order once hitting each important time,
    # This correctly sets the start points for each KeyframeObject,
    # May acc be necessary for render_update as progress==keyframe.get_start() unlikely??
    def bake_starts(self, duration: float):
        key_times = []
        for keyframe in self._keyframes:
            key_times.extend([keyframe.get_start_time(), keyframe.get_end_time()])

        # Sorted may be unnecessary
        key_times = sorted(set(key_times))
        for time in key_times:
            for keyframe in self._keyframes:
                if time >= keyframe.get_end_time():
                    keyframe.update(1, duration)

                # Probably could be if keyframe.get_start() == time
                if keyframe.get_start_time() == time:
                    keyframe.update_start()

        self._last_progress = key_times[-1]
        self._start_baked = True

    # This is complex and inefficient due to the browse ability to skip and go back frames
    # Every update, every previous keyframe is run again
    # Potench create a render_update and browse_update if becomes an issue

    def update(self, progress: float, duration: float):
        if self._keyframes is None:
            # Exit if keyframes have not been attached
            return

        if self._start_baked is False:
            self.bake_starts(duration)

        if progress > self._max_progress:
            self._max_progress = progress

        # Forward time progression
        if progress >= self._last_progress:
            for keyframe in self._keyframes:
                if progress >= keyframe.get_end_time():
                    keyframe.update(1, duration)

                if keyframe.get_start_time() <= progress < keyframe.get_end_time():
                    keyframe.update(progress, duration)
        # Backwards time progression
        else:
            for keyframe in reversed(self._keyframes):
                if progress < keyframe.get_start_time():
                    keyframe.update(0, duration)

                if keyframe.get_start_time() <= progress < keyframe.get_end_time():
                    keyframe.update(progress, duration)

        self._last_progress = progress





