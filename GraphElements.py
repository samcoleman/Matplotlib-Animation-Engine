from FigureElements import FigureElement
import numpy as np
from myMaths import Vec2D

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import sympy
from sympy.abc import x, y


class Cube(FigureElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf):
        super(Cube, self).__init__(start, duration, position, size, mf, '3d', '3d')

        phi = np.arange(1, 10, 2) * np.pi / 4
        self.Phi, self.Theta = np.meshgrid(phi, phi)
        self.x = np.cos(self.Phi) * np.sin(self.Theta)
        self.y = np.sin(self.Phi) * np.sin(self.Theta)
        self.z = np.cos(self.Theta) / np.sqrt(2)

    def _init(self):
        self._axes.set_xlim(-2, 2)
        self._axes.set_ylim(-2, 2)
        self._axes.set_zlim(-2, 2)
        self._my_plot = self._axes.plot_wireframe(self.x, self.y, self.z)
        self._axes.set_axis_off()

    def _update(self, p):
        self._axes.view_init(elev=30., azim=p * 360)
        self._axes.set_anchor((0.5 + p / 2, 0.5))
        self._axes.set_xlim(-2 + p, 2 - p)
        self._axes.set_ylim(-2 + p, 2 - p)
        self._axes.set_zlim(-2 + p, 2 - p)


class Sine(FigureElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf):
        super(Sine, self).__init__(start, duration, position, size, mf, 'rect', 'rectilinear')
        self.x = np.arange(0.0, 2.0, 0.01)

    def _style(self):
        super(Sine, self)._style()
        self._axes.spines["bottom"].set_color('red')

    def _init(self):
        self._my_plot, = self._axes.plot(self.x, 1 + np.sin(self.x), color='white')

    def _update(self, p):
        self._my_plot.set_data(self.x, 1 + np.sin(self.x - p))


def cylinder_stream_function(U=1, R=1):
    r = sympy.sqrt(x ** 2 + y ** 2)
    theta = sympy.atan2(y, x)
    return U * (r - R ** 2 / r) * sympy.sin(theta)


def velocity_field(psi):
    u = sympy.lambdify((x, y), psi.diff(y), 'numpy')
    v = sympy.lambdify((x, y), -psi.diff(x), 'numpy')
    return u, v


class StreamFunction(FigureElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf):
        super(StreamFunction, self).__init__(start, duration, position, size, mf, 'rect', 'rectilinear')

    def _init(self):
        w = 3

        phi = cylinder_stream_function()
        u, v = velocity_field(phi)

        Y, X = np.mgrid[-w:w:100j, -w:w:100j]
        self._axes.set_xlim(-w, w)
        self._axes.set_xlim(-w, w)
        self._my_plot = self._axes.streamplot(X, Y, u(X, Y), v(X, Y), color='k',
                                              linewidth=0.8, density=1.3, minlength=0.9,
                                              arrowstyle='-')
        self._axes.add_patch(Circle((0, 0), radius=1, facecolor='none', edgecolor='white', inewidth=2))

    def _update(self, p):
        return 0

