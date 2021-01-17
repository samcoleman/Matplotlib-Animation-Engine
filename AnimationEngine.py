from os import startfile

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import AnimationElement

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


matplotlib.rcParams['lines.antialiased'] = True
matplotlib.rcParams['patch.antialiased'] = True
matplotlib.rcParams['text.antialiased'] = True
matplotlib.rcParams['text.hinting'] = 'auto'
matplotlib.rcParams['text.hinting_factor'] = 8


def progress_bar(current, total):
    bar_length = 40
    percent = float(current) * 100 / total
    arrow = '#' * int(percent/100 * bar_length)
    spaces = ' ' * (bar_length - len(arrow))

    print('\r', 'Render Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='')


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
        self._fig = plt.figure(figsize=(16, 9))
        self._axes = plt.gca()
        self._axes.set_xlim([-100, 100])
        self._axes.set_ylim([-100, 100])

        self._writer = animation.writers['ffmpeg'](fps=self._fps, codec=None, bitrate=1000)

        self._axes.set_position([0, 0, 1, 1])
        self._axes.set_facecolor('#008cff')
        # self._axes.set_facecolor('black')

    def get_axes(self):
        return self._axes

    def get_fig(self):
        return self._fig

    def add_element(self, elem: AnimationElement):
        self._animElements.append(elem)

    # Runtime in seconds
    def render(self, filename: str, runtime: float):
        with self._writer.saving(self._fig, filename+'.mp4', dpi=self._resolutionY/9):
            for self._frame in range(int(runtime * self._fps)):
                for elem in self._animElements:
                    elem.update(self._frame, self._fps)
                self._writer.grab_frame()
                progress_bar(self._frame + 1, int(runtime * self._fps))
        startfile(filename + '.mp4')
