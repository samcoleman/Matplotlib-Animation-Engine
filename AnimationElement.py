from myMaths import Vec2D


# Animation Element, start time and end time
class AnimationElement:
    def __init__(self, start: float, duration: float, position: Vec2D):
        self._instantiated = False

        self._start = start
        self._end = start + duration
        self._position = position

    def update(self, frame, fps):
        # Progress from 0-1
        # Minus one start/end zero indexed so last frame object is not shown
        progress = (frame - (self._start * fps)) / (((self._end - self._start) * fps) - 1)

        # ACTIVE
        if self._start * fps <= frame < self._end * fps:
            # If active and not instantiated, instantiate!
            if not self._instantiated:
                self._instantiated = True
                return self._instantiate()
            # Update element with progress state
            try:
                return self._update(progress)
            except Exception as detail:
                print("Error:", detail)
            return None

        # INACTIVE
        else:
            # If inactive and instantiated clean-up
            if self._instantiated:
                try:
                    self._instantiated = False
                    return self._cleanup()
                except Exception as detail:
                    print("Error:", detail)
                return None

    def _instantiate(self):
        raise Exception("Element Instantiate Not Implemented")

    def _update(self, progress):
        raise Exception("Element Update Not Implemented")

    def _cleanup(self):
        raise Exception("Element Cleanup Not Implemented")
