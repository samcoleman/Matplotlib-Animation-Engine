from AnimationEngine import AnimationEngine
from AnimationElement import *
import math

import numpy as np

import Figures as fgs


def fn(t, p):
    return 1 + np.sin(t-p)


if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)

    main_fig, main_axes = ae.get_fig()

    ae.add_element(TextElement(main_axes, 0, 10, Vec2D(0, 75), 'Top', horizontalalignment='center',
                               verticalalignment='center', color='white', fontsize=72))

    ae.add_element(TextElement(main_axes, 0, 10, Vec2D(0, -75), 'Bottom', horizontalalignment='center',
                               verticalalignment='center', color='white', fontsize=72))

    ae.add_element(FigElement(main_axes, 3, 5, Vec2D(0, 0), fgs.FigureObj3D(main_fig)))
    ae.add_element(FigElement(main_axes, 3, 5, Vec2D(0, 0), fgs.FigureObj2D(main_fig, fn)))

    ae.browse()
    #ae.render('test2', 10)
