from os import startfile
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from celluloid import Camera

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

        self._axes.set_position([0, 0, 1, 1])
        self._axes.set_facecolor('#008cff')

    def get_axes(self):
        return self._axes

    def add_element(self, elem: AnimationElement):
        self._animElements.append(elem)

    # Runtime in seconds
    def animate(self, runtime: float):
        for self._frame in range(int(runtime * self._fps)):
            for elem in self._animElements:
                elem.update(self._frame, self._fps)
            self._camera.snap()

    def save(self, filename: str):
        writer = animation.writers['ffmpeg'](fps=self._fps)
        anim = self._camera.animate()
        anim.save(filename + '.mp4', writer=writer, dpi=self._resolutionY)
        startfile(filename + '.mp4')
