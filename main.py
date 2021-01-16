from AnimationEngine import AnimationEngine

from AnimationElement import *


import numpy as np


class Figure:
    def __init__(self):

        # Data for plotting
        self.t = np.arange(0.0, 2.0, 0.01)

    def plot(self, progress):
        self.axes.plot(self.t, 1 + np.sin(2 * np.pi * (self.t - progress)), color='white')


if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)
    axes = ae.get_axes()

    ae.add_element(TextElement(axes, 5, 10, Vec2D(0, 75), 'Hello', horizontalalignment='center',
                               verticalalignment='center', color='white'))

    ae.add_element(FigElement(axes, 3, 8, Vec2D(0, 0), Figure()))
    ae.animate(10)
    ae.save('test2')
