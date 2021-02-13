from Engine.Elements.AxesElement import AxesElement, AxesData
import numpy as np
from Engine.MathsHelpers import Vec2D


class Cube(AxesElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf):
        ad = AxesData(projection='3d', xlim=[-2, 2], ylim=[-2, 2], zlim=[-2, 2], axes_on=True)
        super(Cube, self).__init__(start, duration, position, size, mf, '3d', ad)

        phi = np.arange(1, 10, 2) * np.pi / 4
        self.Phi, self.Theta = np.meshgrid(phi, phi)
        self.x = np.cos(self.Phi) * np.sin(self.Theta)
        self.y = np.sin(self.Phi) * np.sin(self.Theta)
        self.z = np.cos(self.Theta) / np.sqrt(2)

    def _init(self):
        self._my_plot = self._axes.plot_wireframe(self.x, self.y, self.z)

    def _refresh(self, p):
        self._axes.view_init(elev=30., azim=p * 360)


class Sine(AxesElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf):
        super(Sine, self).__init__(start, duration, position, size, mf, 'rect', AxesData(autoscale=True))
        self.x = np.arange(0.0, 2.0, 0.01)

    def _style(self):
        super(Sine, self)._style()

    def _init(self):
        self._my_plot, = self._axes.plot(self.x, 1 + np.sin(self.x), color='white')

    def _refresh(self, p):
        self._my_plot.set_data(self.x, 1 + np.sin(self.x - p))





