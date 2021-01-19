from AnimationElement import AnimationElement
from myMaths import Vec2D

import numpy as np


class Figure2DElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D,
                 main_fig, fn):
        AnimationElement.__init__(self, start, duration, position)
        self._main_fig = main_fig
        # Data for plotting
        self.t = np.arange(0.0, 2.0, 0.01)
        self.fn = fn

    def _inset(self):
        self._axes = self._main_fig.add_axes([0.1, 0.1, 0.8, 0.8], label='2D', anchor='C', projection='rectilinear')

    def _style(self):
        self._axes.patch.set_alpha(0)
        self._axes.spines["top"].set_color('white')
        self._axes.spines["bottom"].set_color('white')
        self._axes.spines["left"].set_color('white')
        self._axes.spines["right"].set_color('white')
        self._axes.tick_params(axis='x', colors='white')
        self._axes.set_xlabel("x-label", color="white")
        self._axes.tick_params(axis='y', colors='white')
        self._axes.set_xlabel("y-label", color="white")

    def _instantiate(self):
        print("F2")
        self._inset()
        self._style()
        self._my_plot, = self._axes.plot(self.t, self.fn(self.t, 0), color='white')
        self._axes.set_axis_on()
        return 0

    def _update(self, progress):
        print("u")
        self._my_plot.set_data(self.t, self.fn(self.t, progress))
        return 0

    def _cleanup(self):
        self._axes.remove()
        return 0

def get_cube():
    phi = np.arange(1,10,2)*np.pi/4
    Phi, Theta = np.meshgrid(phi, phi)

    x = np.cos(Phi)*np.sin(Theta)
    y = np.sin(Phi)*np.sin(Theta)
    z = np.cos(Theta)/np.sqrt(2)
    return x,y,z


class Figure3DElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D,
                 main_fig):
        AnimationElement.__init__(self, start, duration, position)
        self._fig = main_fig

        self.x, self.y, self.z = get_cube()

    def _inset(self):
        self._axes = self._fig.add_axes([0.1, 0.1, 0.8, 0.8], label='3D', anchor='C', projection='3d')

    def _style(self):
        self._axes.patch.set_alpha(0)

    def _instantiate(self):
        print("F3")
        self._inset()
        self._style()
        self._axes.set_xlim(-2, 2)
        self._axes.set_ylim(-2, 2)
        self._axes.set_zlim(-2, 2)
        self._my_plot = self._axes.plot_wireframe(self.x, self.y, self.z)
        self._axes.set_axis_off()
        return 0

    def _update(self, progress):
        print("u")
        self._axes.view_init(elev=30., azim=progress*360)
        self._axes.set_anchor((0.5+progress/2, 0.5))
        self._axes.set_xlim(-2+progress, 2-progress)
        self._axes.set_ylim(-2+progress, 2-progress)
        self._axes.set_zlim(-2+progress, 2-progress)
        return 0

    def _cleanup(self):
        self._my_plot.remove()
        return 0
