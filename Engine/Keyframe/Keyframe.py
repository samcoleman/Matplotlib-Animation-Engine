from typing import List, Union, Callable
import operator

from matplotlib.axes import Axes
from matplotlib.text import Text


def clamp(n: float, minn: float, maxn: float) -> float:
    return max(min(maxn, n), minn)


class KeyframeObject:
    def __init__(self) -> None:
        self._handle: any = None
        self._set_s = False

        # Initial Value
        self._i_value: any = None
        # Final Value
        self._f_value: any = None

    def _interp(self, adj_progress: float) -> any:
        return self._i_value + (self._f_value - self._i_value) * adj_progress

    def attach_handle(self, h: any) -> None:
        # Only attach handle if there is not one already, this is used for parameters to ensure not overwritten
        if self._handle is None:
            self._handle = h

    def set_start(self) -> None:
        self._set_start()
        self._post_start()

    def _set_start(self) -> None:
        return

    def _post_start(self) -> None:
        return

    def update(self, adj_progress: float, duration: float) -> None:
        self._update(adj_progress, duration)
        self._post_update(adj_progress, duration)

    # This function is triggered when current frame is moved backwards during browse and Parameter needs to return
    # to original state (called after update)
    def reset(self) -> None:
        return

    def _update(self, adj_progress: float, duration: float) -> None:
        return

    def _post_update(self, adj_progress: float, duration: float) -> None:
        return


class KeyFrame:
    def __init__(self, keyobjs: List[KeyframeObject], end_t: float, start_t: Union[float, None] = None,
                 fn: Callable[[float], float] = lambda y: y) -> None:
        self._update_start_called = False
        self._key_objs = keyobjs
        self._start_t = start_t
        self._end_t = end_t
        self._fn = fn

    def set_start_time(self, start: float) -> None:
        self._start_t = start

    def get_start_time(self) -> float:
        return self._start_t

    def get_end_time(self) -> float:
        return self._end_t

    def attach_handle(self, h: any) -> None:
        for key in self._key_objs:
            key.attach_handle(h)

    def update_start(self) -> None:
        if self._update_start_called is False:
            for key in self._key_objs:
                key.set_start()
        else:
            print("repeat start call")

            self._update_start_called = True

    def update(self, progress: float, duration: float) -> None:
        adjusted_progress = clamp((progress - self._start_t)/(self._end_t-self._start_t), 0, 1)

        for key in self._key_objs:
            # Hmm might cause problems for duration? Not that im using for alt yet
            key.update(self._fn(adjusted_progress), duration)

        # When keyframeObjs are needed to reset from browse going backwards
        if progress == -1:
            for key in self._key_objs:
                key.reset()


class KeyFrameManager:
    def __init__(self):
        self._sequence: List[KeyFrame] = []
        self._last_progress, self._max_progress = 0, 0
        self._start_baked = False

    def attach_sequence(self, new_sequence: List[KeyFrame]) -> None:
        # Setup the start time for each keyframe if not already set, allows for quick keyframing
        for i in range(len(new_sequence)):
            if new_sequence[i].get_start_time() is None:
                if i == 0:
                    # Set start time to 0 if the first item
                    new_sequence[i].set_start_time(0)
                else:
                    # Otherwise set to the end-time of previous keyframe
                    new_sequence[i].set_start_time(new_sequence[i - 1].get_end_time())

        # Sort keyframe so they appear in ascending order by _start_t
        # Should help resolve user input errors and be more consistent
        self._sequence.extend(new_sequence)
        self._sequence = sorted(self._sequence, key=operator.attrgetter('_start_t'))
        # Inplace sort, use if memory is a problem but really doubt it
        #x.sort(key=operator.attrgetter('score'))

    def attach_handle(self, h: Union[None, Axes, Text]) -> None:
        if len(self._sequence) == 0:
            # Cannot attach handles if keyframes don't exist
            return
        for key in self._sequence:
            key.attach_handle(h)

    # The whole sequence is run through in order once hitting each important time,
    # This correctly sets the start points for each KeyframeObject,
    # May acc be necessary for render_update as progress==keyframe.get_start() unlikely??
    def bake_starts(self, duration: float) -> None:
        key_times = []
        for keyframe in self._sequence:
            key_times.extend([keyframe.get_start_time(), keyframe.get_end_time()])

        # Sorted may be unnecessary
        key_times = sorted(set(key_times))
        for time in key_times:
            for keyframe in self._sequence:
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

    def update(self, progress: float, duration: float) -> None:
        if len(self._sequence) == 0:
            # Exit if keyframes have not been attached
            return

        if self._start_baked is False:
            self.bake_starts(duration)

        if progress > self._max_progress:
            self._max_progress = progress

        # Forward time progression
        if progress >= self._last_progress:
            for keyframe in self._sequence:
                if progress >= keyframe.get_end_time():
                    keyframe.update(1, duration)

                if keyframe.get_start_time() <= progress < keyframe.get_end_time():
                    keyframe.update(progress, duration)
        # Backwards time progression
        else:
            for keyframe in reversed(self._sequence):
                if progress < keyframe.get_start_time():
                    # -1 not 0 so it can signify to the component to reset to original value
                    keyframe.update(-1, duration)

                if keyframe.get_start_time() <= progress < keyframe.get_end_time():
                    keyframe.update(progress, duration)

        self._last_progress = progress





