from AnimationEngine import AnimationEngine
from BasicElements import *
from FigureElements import *

import numpy as np


def fn(t, p):
    return 1 + np.sin(t-p)


if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)

    main_fig, main_axes = ae.get_fig()

    ae.add_element(TextElement(0, 10, Vec2D(0, 75), main_axes, 'Top', horizontalalignment='center',
                               verticalalignment='center', color='white', fontsize=72))

    ae.add_element(TextElement(0, 10, Vec2D(0, -75), main_axes, 'Bottom', horizontalalignment='center',
                               verticalalignment='center', color='white', fontsize=72))

    ae.add_element(Figure2DElement(3, 5, Vec2D(0, 0), main_fig, fn))
    ae.add_element(Figure2DElement(0, 10, Vec2D(0, 0), main_fig, fn))
    ae.add_element(Figure3DElement(3, 5, Vec2D(0, 0), main_fig))

    ae.browse()
    # ae.render('test2', 10)
