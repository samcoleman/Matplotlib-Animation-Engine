from Engine.Elements.AxesElement import AxesElement, AxesData, AxesStyle
import numpy as np
from Engine.MathsHelpers import Vec2D
from Engine.Keyframe.Parameter import Parameter


class Cube(AxesElement):
    def __init__(self, position: Vec2D, size: Vec2D,
                 axes_data: AxesData = AxesData(), axes_style: AxesStyle = AxesStyle()):
        axes_data.projection = '3d'

        super(Cube, self).__init__(position, size, 'Cube', axes_data, axes_style)

        phi = np.arange(1, 10, 2) * np.pi / 4
        self.Phi, self.Theta = np.meshgrid(phi, phi)
        self.x = np.cos(self.Phi) * np.sin(self.Theta)
        self.y = np.sin(self.Phi) * np.sin(self.Theta)
        self.z = np.cos(self.Theta) / np.sqrt(2)

    def _instantiate(self):
        self._my_plot = self._axes.plot_wireframe(self.x, self.y, self.z, color='white')

    def _update(self, progress: float, duration: float):
        self._axes.view_init(elev=30., azim=progress * 360)


class Sine(AxesElement):
    def __init__(self, position: Vec2D, size: Vec2D,
                 axes_data: AxesData = AxesData(), axes_style: AxesStyle = AxesStyle()):
        super(Sine, self).__init__(position, size, "Sine", axes_data, axes_style)
        self.x = np.arange(-2.0, 2.0, 0.01)

    def _instantiate(self):
        self._my_plot, = self._axes.plot(self.x, np.sin(self.x), color='white')

    def _update(self, progress: float, duration: float):
        self._my_plot.set_data(self.x, np.sin(self.x - progress))





