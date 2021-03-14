from os import startfile

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

from Engine.Theme import Theme
from Engine.Keyframe.Parameter import GlobalParameterManager
from Engine.Elements import AnimationElement

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


matplotlib.rcParams['lines.antialiased'] = True
matplotlib.rcParams['patch.antialiased'] = True
matplotlib.rcParams['text.antialiased'] = True
matplotlib.rcParams['text.hinting'] = 'auto'
matplotlib.rcParams['text.hinting_factor'] = 8

# Support Latex just very slow
# matplotlib.rc('text', usetex=True)


def progress_bar(current, total, elem, axes):
    bar_length = 40
    percent = float(current) * 100 / total
    arrow = '#' * int(percent/100 * bar_length)
    spaces = ' ' * (bar_length - len(arrow))

    print('\r', 'Render Progress: [%s%s] %d %% Elements: %s Axes: %s' % (arrow, spaces, percent, elem, axes), end='')


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
        self._axes.set_xlim([0, 1])
        self._axes.set_ylim([0, 1])

        self._writer = animation.writers['ffmpeg'](fps=self._fps, codec=None, bitrate=8000)

        self._axes.set_position([0, 0, 1, 1])
        self._axes.set_facecolor(Theme.color.primary)

        self._global_parameter_manager = GlobalParameterManager()

    def get_ar(self):
        return self._aspectRatio

    def add_element(self, elem: AnimationElement, start: float, duration: float):
        elem.attach_timings(start, start+duration)
        elem.attach_main_scene(self._fig, self._axes)
        # Creates a unique instance name for the element which is human readable
        inst_name = type(elem).__name__+str(sum(type(elem).__name__ == type(e).__name__ for e in self._animElements))
        elem.attach_parameter_manager(inst_name, self._global_parameter_manager)
        self._animElements.append(elem)
        return elem

    def _update_element(self, elem: AnimationElement):
        start_time, end_time = elem.get_timings()
        duration = end_time - start_time

        # Progress from 0-1
        # Minus one start/end zero indexed so last frame object is not shown
        progress = (self._frame - (start_time * self._fps)) / ((duration * self._fps) - 1)
        # ACTIVE
        if start_time * self._fps <= self._frame < end_time * self._fps:
            elem.update(progress, duration)
        # INACTIVE
        else:
            elem.cleanup()

    def _update_elements(self):
        for elem in self._animElements:
            self._update_element(elem)

    def _slider_update(self, val):
        self._frame = val
        self._update_elements()
        self._fig.canvas.draw()

    def browse(self, runtime: float):
        frame_slider_ax = self._fig.add_axes([0.25, 0.1, 0.65, 0.03], label='frame_slider', facecolor='black', zorder=10000)
        frame_slider = Slider(frame_slider_ax, 'Frame', 0, int(runtime * self._fps) - 1, valinit=0, valstep=1)
        self._update_elements()
        frame_slider.on_changed(self._slider_update)
        plt.show()

    # Runtime in seconds
    def render(self, filename: str, runtime: float):
        self._frame = 0
        with self._writer.saving(self._fig, filename+'.mp4', dpi=self._resolutionY/9):
            for self._frame in range(int(runtime * self._fps)):
                self._update_elements()
                self._writer.grab_frame()
                progress_bar(self._frame + 1, int(runtime * self._fps), len(self._animElements), len(self._fig.axes))
        startfile(filename + '.mp4')
