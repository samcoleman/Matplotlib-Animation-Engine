from AnimationEngine import AnimationEngine
from BasicElements import *
from GraphElements import *

import sympy
from sympy.abc import x, y

from typing import List, Tuple
from myMaths import Vec3D

def cylinder_stream_function(U=1, R=1):
    r = sympy.sqrt(x ** 2 + y ** 2)
    theta = sympy.atan2(y, x)
    return U * (r - R ** 2 / r) * sympy.sin(theta)


if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)

    ar = ae.get_ar()

    main_fig, main_axes = ae.get_fig()

    sequence = [(Translate2D(Vec2D(.75, .75)), .5),
                ([Translate2D(Vec2D(.75, .25)),
                  Scale(32),
                  Rotate(45)], 1.)]

    sequence2 = [([Translate2D(Vec2D(.25, .25)),
                  Scale2D(Vec2D(.5/ar, .5))], 1.)]

    #ae.add_element(TextElement(0, 10, Vec2D(.5, .75), main_axes, "Hello", 72, sequence,
    #                           horizontalalignment='center', verticalalignment='center', color='white'))

    ae.add_element(StreamFunction(0, 10, Vec2D(.1, .1), Vec2D(.8/ar, .8),
                                  main_fig, cylinder_stream_function, sequence2))

    ae.browse()

    #ae.render('test2', 10)
