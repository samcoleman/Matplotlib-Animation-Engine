from AnimationEngine import AnimationEngine
from BasicElements import *
from FigureElements import *

import numpy as np


class Sine(Figure2DElement):
    def __init__(self, start: float, duration: float, position: Vec2D, mf):
        super().__init__(start, duration, position, mf)
        self.x = np.arange(0.0, 2.0, 0.01)

    def fn(self, p):
        return self.x, 1 + np.sin(self.x - p)


class Cube(Figure3DElement):
    def __init__(self, start: float, duration: float, position: Vec2D, mf):
        super().__init__(start, duration, position, mf)
        phi = np.arange(1, 10, 2) * np.pi / 4
        self.Phi, self.Theta = np.meshgrid(phi, phi)

    def fn(self, p):

        x = np.cos(self.Phi) * np.sin(self.Theta)
        y = np.sin(self.Phi) * np.sin(self.Theta)
        z = np.cos(self.Theta) / np.sqrt(2)
        return x, y, z


if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)

    main_fig, main_axes = ae.get_fig()

    ae.add_element(TextElement(0, 10, Vec2D(0, 75), main_axes, 'Top', horizontalalignment='center',
                               verticalalignment='center', color='white', fontsize=72))

    ae.add_element(TextElement(0, 10, Vec2D(0, -75), main_axes, 'Bottom', horizontalalignment='center',
                               verticalalignment='center', color='white', fontsize=72))

    ae.add_element(Sine(1, 10, Vec2D(0, 0), main_fig))
    ae.add_element(Cube(3, 5, Vec2D(0, 0), main_fig))

    ae.browse()
    # ae.render('test2', 10)
