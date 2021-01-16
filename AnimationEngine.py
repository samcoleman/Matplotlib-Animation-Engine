from os import startfile
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import AnimationElement


class AnimationEngine:

    # yResolution in 480, 720, 1080 ect
    def __init__(self, resolution: int, fps: int):
        self._frame = 0
        self._animElements = []

        self._aspectRatio = 16 / 9

        self._resolutionX = resolution * self._aspectRatio
        self._resolutionY = resolution
        self._fps = fps

        # Setup frame & camera
        self._fig = plt.figure(figsize=(self._aspectRatio, 1))
        self._axes = plt.gca()
        self._axes.set_xlim([-100, 100])
        self._axes.set_ylim([-100, 100])
        self._camera = Camera(self._fig)

        self._writer = animation.writers['ffmpeg'](fps=self._fps)

        self._axes.set_position([0, 0, 1, 1])
        self._axes.set_facecolor('#008cff')

    def get_axes(self):
        return self._axes

    def add_element(self, elem: AnimationElement):
        self._animElements.append(elem)

    # Runtime in seconds
    def animate(self, filename: str, runtime: float):
        with self._writer.saving(self._fig, filename+'.mp4', dpi=self._resolutionY):
            for self._frame in range(int(runtime * self._fps)):
                for elem in self._animElements:
                    elem.update(self._frame, self._fps)
                self._writer.grab_frame()
